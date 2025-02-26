odoo.define('aos_whatsapp_pos.ReceiptScreen', function(require) {
	"use strict";

    const { Printer } = require('point_of_sale.Printer');
	const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');

    const { onMounted, useRef, status } = owl;

    const WhatsappReceiptScreen = ReceiptScreen =>
        class extends ReceiptScreen {
			constructor() {
				super(...arguments);
				let self = this;
                //this.orderReceiptWhatsApp = useRef('order-receipt');
                this.orderReceipt = useRef('order-receipt');
                const order = this.currentOrder;
                const client = order.get_partner();
            	const orderName = order.get_name();

				const pos_config = this.env.pos.config;
				let message = pos_config.whatsapp_default_message.replace("_CUSTOMER_", client && client.name || 'Customer');
				//console.log('==WhatsappReceiptScreen=1=',orderName,client.name)
				//console.log('==WhatsappReceiptScreen=2=',pos_config.whatsapp_default_message)
                //this.orderUiState = useContext(order.uiState.ReceiptScreen);
                this.orderUiState = order.uiState.ReceiptScreen;
                //this.orderUiState.inputWhatsapp = order.orderUiState.inputWhatsapp || (client && client.whatsapp) || '';
                this.orderUiState.inputWhatsapp = this.orderUiState.inputWhatsapp || (client && client.whatsapp) || '';
                this.orderUiState.inputMessage = message + ' ' + orderName +'.';
			}
			async is_whatsapp(value) {
                const order = this.currentOrder;
                const session = order.pos_session_id;
				//console.log('==value==',order.pos_session_id,value)
	            var result = await this.rpc({
	                model: 'pos.order',
	                method: 'get_number_exist',
	                args: [[], session, value],
	            });	
	            return result;
	        }
            async onSendWhatsapp() {
                const config = this.env.pos.config;
                if (!config.whatsapp_server_id) {
                    this.orderUiState.whatsappSuccessful = false;
                    this.orderUiState.whatsappNotice = this.env._t('Whatsapp server should define first!.');
                    return;
                }
				let whatsapp = true;//await this.is_whatsapp(this.orderUiState.inputWhatsapp);
				//console.log('==',whatsapp)
                if (!whatsapp) {
                    this.orderUiState.whatsappSuccessful = false;
                    this.orderUiState.whatsappNotice = this.env._t('Whatsapp number is empty / not valid.');
                    return;
                }
                try {
                    await this._sendWhatsappToCustomer();
                    this.orderUiState.whatsappSuccessful = true;
                    this.orderUiState.whatsappNotice = 'Whatsapp sent.'
                } catch (error) {
					//console.log('==error==',error)
                    this.orderUiState.whatsappSuccessful = false;
                    this.orderUiState.whatsappNotice = 'Sending Whatsapp failed. Please try again.'
                }
                //console.log('=onSendWhatsapp=',this._sendWhatsappToCustomer())
            }
            
            async _sendWhatsappToCustomer() {
				console.log('START=xx>')
                const printer = new Printer(null, this.env.pos);
                const receiptString = this.orderReceipt.el.innerHTML;
                const ticketImage = await printer.htmlToImg(receiptString);
                const order = this.currentOrder;
                const partner = order.get_partner();
                const orderName = order.get_name();
                const orderPartner = { whatsapp: this.orderUiState.inputWhatsapp, message: this.orderUiState.inputMessage, name: partner ? partner.name : this.orderUiState.inputWhatsapp };
                const order_server_id = this.env.pos.validated_orders_name_server_id_map[orderName];
                await this.rpc({
                    model: 'pos.order',
                    method: 'action_whatsapp_to_customer',
                    args: [[order_server_id], orderName, orderPartner, ticketImage],
                });
				console.log('--END=>')
            }
		};

	Registries.Component.extend(ReceiptScreen, WhatsappReceiptScreen);

	return ReceiptScreen;

});

