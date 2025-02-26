odoo.define('aos_whatsapp_pos.PartnerDetailsEdit', function (require) {
    'use strict';

    const { _t } = require('web.core');
    // const PosComponent = require('point_of_sale.PosComponent');
    const PartnerDetailsEdit = require('point_of_sale.PartnerDetailsEdit');
    // const PosComponent = require('point_of_sale.PosComponent');
    // const {useState} = owl.hooks;
    const { onMounted, useState, onWillUnmount } = owl;
    // const {useListener} = require('web.custom_hooks');
    // const models = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    //class PartnerDetailsEdit extends PosComponent
    
    const WhatsappPartnerDetailsEdit = PartnerDetailsEdit =>
        class extends PartnerDetailsEdit {
			// constructor() {
			// 	super(...arguments);
			// }
            setup() {
                super.setup();
                this.intFields = ["country_id", "state_id", "property_product_pricelist"];
                const partner = this.props.partner;
                this.changes = useState({
                    name: partner.name || "",
                    street: partner.street || "",
                    city: partner.city || "",
                    zip: partner.zip || "",
                    state_id: partner.state_id && partner.state_id[0],
                    country_id: partner.country_id && partner.country_id[0],
                    lang: partner.lang || "",
                    email: partner.email || "",
                    phone: partner.phone || "",
                    mobile: partner.mobile || "",
                    whatsapp: partner.whatsapp || "",
                    barcode: partner.barcode || "",
                    vat: partner.vat || "",
                    property_product_pricelist: this.getDefaultPricelist(partner),
                });
    
            //     onMounted(() => {
            //         this.env.bus.on("save-partner", this, this.saveChanges);
            //     });
    
            //     onWillUnmount(() => {
            //         this.env.bus.off("save-partner", this);
            //     });
            }
            getDefaultPricelist(partner) {
                if (partner.property_product_pricelist) {
                    return partner.property_product_pricelist[0];
                }
                return this.env.pos.default_pricelist ? this.env.pos.default_pricelist.id : false;
            }
            // captureChange(event) {}
            saveChanges() {
                let processedChanges = {};
                for (let [key, value] of Object.entries(this.changes)) {
                    if (this.intFields.includes(key)) {
                        processedChanges[key] = parseInt(value) || false;
                    } else {
                        processedChanges[key] = value;
                    }
                }
                if ((!this.props.partner.name && !processedChanges.name) ||
                    processedChanges.name === '' ){
                    return this.showPopup('ErrorPopup', {
                      title: _t('A Customer Name Is Required'),
                    });
                }
                // console.log('==this.changes==',this.changes)
                // console.log('==Name==',processedChanges.name,this.props.partner.name)
                // console.log('==Whatsapp==',processedChanges.whatsapp,this.props.partner.whatsapp)
                if ((!this.props.partner.whatsapp && !processedChanges.whatsapp) ||
                    processedChanges.whatsapp === '' ){
                    return this.showPopup('ErrorPopup', {
                      title: _t('A Whatsapp Number Is Required or Cannot 0'),
                    });
                }
                processedChanges.id = this.props.partner.id || false;
                this.trigger('save-changes', { processedChanges });
            }
		};
    Registries.Component.extend(PartnerDetailsEdit, WhatsappPartnerDetailsEdit);

    return WhatsappPartnerDetailsEdit;
});
