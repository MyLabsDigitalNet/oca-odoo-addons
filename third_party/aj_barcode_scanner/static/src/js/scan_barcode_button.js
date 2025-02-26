odoo.define('aj_barcode_scanner.ScanBarcodeButton', function(require) {
   'use strict';
   const PosComponent = require('point_of_sale.PosComponent');
   const { useListener } = require("@web/core/utils/hooks");
   const Registries = require('point_of_sale.Registries');
   const {  useState } = owl;


   class ScanBarcodeButton extends PosComponent {

        setup() {
            super.setup();
            useListener('click', this.onClick);
            this.state = useState({
                started: false,
                html5QrCode: null,
                scanning:false,
            });
        }

        async start_scanner(cameraId){
            var self = this;
            var sound = document.getElementById("audio");
            var scan_div = document.getElementById("scan_reader");
            var root_scan_div = document.getElementById("root_scan_reader");

            function delay(time) {
                    return new Promise(resolve => setTimeout(resolve, time));
                }


            var config
            if (self.env.isMobile){
                config = { fps: 10 ,qrbox: 200 ,aspectRatio: 1 };
                //scan_div.style.width = "100%";
                //scan_div.style.display = "block";
                root_scan_div.style.width = "100%";
                root_scan_div.style.display = "block";

            }
            else{
                config = { fps: 10 ,qrbox: 200 ,aspectRatio: 1.33 };
                //scan_div.style.width = "600px";
                //scan_div.style.display = "block";
                root_scan_div.style.width = "600px";
                root_scan_div.style.display = "block";
            }
            //console.log(`Start Scanner`);
            await self.state.html5QrCode.start(
                cameraId, 
                config,
                async (decodedText, decodedResult) => {
                if(!self.state.scanning){
                    self.state.scanning = true;
                    
                    sound.play();
                    await self.env.barcode_reader.scan(decodedText);           

                    await delay(1000);
                    self.state.scanning = false;
                }

            },
            (errorMessage) => {
                // parse error, ignore it.
            })
            .catch((err) => {
                console.log("faild to start scanner "+err)
            });


            var close_btn = document.createElement("button");
            close_btn.style.position = "absolute";
            close_btn.style.top = "40px";
            close_btn.style.right = "80px";
            close_btn.style.width = "80%";
            close_btn.style.height = "80%";
            close_btn.style.zIndex = "101";
            close_btn.style.backgroundColor = "transparent";
            close_btn.style.border = "none";
            close_btn.style.color = "black";
            close_btn.style.fontSize = "20px";
            close_btn.style.fontWeight = "bold";
            close_btn.style.cursor = "pointer";
            close_btn.onclick = async function () {
                //console.log("close clicked");
                self.state.started = false;
                self.state.html5QrCode.stop().then((ignore) => {

                    root_scan_div.style.width = "0px";
                    root_scan_div.style.display = "none";
                    scan_div.innerHTML = "";
                }).catch((err) => {
                    // Stop failed, handle it.
                    console.log("stop failed");
                });
            };
            scan_div.appendChild(close_btn);


            let settings = self.state.html5QrCode.getRunningTrackSettings();
            //console.log(settings);
            if("torch" in settings){
            var torch_btn = document.createElement("button");
            torch_btn.innerHTML = '<i class="fa fa-lightbulb-o " aria-hidden="true"></i>';

            torch_btn.style.position = "absolute";
            torch_btn.style.top = "10px";
            torch_btn.style.right = "10px";
            torch_btn.style.zIndex = "100";
            torch_btn.style.backgroundColor = "transparent";
            torch_btn.style.border = "none";
            torch_btn.style.color = "white";
            torch_btn.style.fontSize = "40px";
            torch_btn.style.fontWeight = "bold";
            torch_btn.style.cursor = "pointer";
            torch_btn.classList.add("camera_torch");
            torch_btn.onclick = async function () {
                //console.log("torch clicked");
                let settings = self.state.html5QrCode.getRunningTrackSettings();
                //console.log(settings);
                if("torch" in settings){
                if (settings.torch !== true) {
                    let constraints = {
                        "torch": true,
                        "advanced": [{ "torch": true }]
                    };
                    await self.state.html5QrCode.applyVideoConstraints(constraints);
                    // let settings = html5Qrcode.getRunningTrackSettings();
                }
                else {
                    let constraints = {
                        "torch": false,
                        "advanced": [{ "torch": false }]
                    };
                    await self.state.html5QrCode.applyVideoConstraints(constraints);
                    // let settings = html5Qrcode.getRunningTrackSettings();
                }
            }
            };
            scan_div.appendChild(torch_btn);
        }

            var svg_div2 = document.createElement("img"); 
            svg_div2.width = "10";
            svg_div2.height = "10";
            svg_div2.src = "/aj_barcode_scanner/static/src/img/black.png";
            svg_div2.alt = "black sqr";
            svg_div2.style.position = "absolute";
            svg_div2.style.top = "10px";
            svg_div2.style.right = "10px";
            svg_div2.classList.add("rotate_box");
            
            
            svg_div2.style.color = "white";
            svg_div2.style.zIndex = "202";


            scan_div.appendChild(svg_div2);

        }

        async onClick() {

            var self = this;
            var scan_div = document.getElementById("scan_reader");
            var root_scan_div = document.getElementById("root_scan_reader");
            var setting_scan_div = document.getElementById("setting_scan_reader");

            if(self.state.started){
                // console.log("scan started");
                self.state.started = false;
                self.state.html5QrCode.stop().then((ignore) => {
                    scan_div.innerHTML = "";
                    root_scan_div.style.width = "0px";
                    root_scan_div.style.display = "none";
                }).catch((err) => {
                    // Stop failed, handle it.
                    console.log("stop scanner failed "+err);
                });

            }
            else{
                self.state.started = true;

                self.state.html5QrCode = new Html5Qrcode("scan_reader",
                    { formatsToSupport: [Html5QrcodeSupportedFormats.EAN_13, Html5QrcodeSupportedFormats.CODE_128, Html5QrcodeSupportedFormats.CODE_39, Html5QrcodeSupportedFormats.EAN_8,Html5QrcodeSupportedFormats.QR_CODE] } );


                

                Html5Qrcode.getCameras().then(devices => {


                    //console.log(devices);
                    if (devices && devices.length) {

                        var current_device_idx = localStorage.getItem("current_device_idx");
                        if(current_device_idx){
                            current_device_idx = parseInt(current_device_idx);
                        }
                        else{
                            current_device_idx = 0;
                        }
                        var cameraId = devices[current_device_idx].id;

                        var cameras_options = document.createElement("select");
                        setting_scan_div.innerHTML = "";
                        devices.forEach((element, idx, arr) => {
                            cameras_options.options.add( new Option(element.label , idx) )
                            if(idx == current_device_idx){
                                cameras_options.options[idx].selected = true;
                            }
                            
                        });

                        cameras_options.onchange = function(){
                            cameraId = devices[this.value].id;
                            current_device_idx = this.value;
                            localStorage.setItem("current_device_idx", current_device_idx);
                            restart_scanner(cameraId)
                            //console.log(cameraId);

                        }

                        cameras_options.style.marginBottom = "10px";
                        cameras_options.style.marginRight = "10px";

                        setting_scan_div.appendChild(cameras_options);

                        function restart_scanner(cameraId){
                            self.state.html5QrCode.stop().then((ignore) => {
                                self.start_scanner(cameraId);
                            }).catch((err) => {
                                // Stop failed, handle it.
                                console.log("stop scanner failed "+err);
                            });
                        }

                        self.start_scanner(cameraId);

                    }
                }).catch(err => {
                 console.log(`get cameras faild ` + err)
                });
 

                               
                
            }
        }

    }
    ScanBarcodeButton.template = 'ScanBarcodeButton';

    Registries.Component.add(ScanBarcodeButton);

    return ScanBarcodeButton;
});