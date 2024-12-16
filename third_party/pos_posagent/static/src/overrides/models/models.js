/** @odoo-module */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    after_load_server_data() {
        var self = this;
        return super.after_load_server_data(...arguments).then(function () {
            if (self.config.use_posagent) {
                self.config.iface_print_via_proxy  = self.config.posagent_enable_printer;
                self.config.iface_cashdrawer = self.config.posagent_enable_cash_drawer;
                if (self.config.use_posagent && (self.config.posagent_enable_printer)) {
                    self.config.is_posbox = true;
                    self.config.use_proxy = true;
                    if (self.config.posagent_enable_printer) self.config.iface_print_via_proxy = true;
                    if (self.config.posagent_enable_cashdrawer) self.config.iface_cashdrawer = true;
                    self.config.iface_customer_facing_display_via_proxy = false;
                    self.config.iface_scan_via_proxy = false;
                    self.config.iface_electronic_scale = false;
                    self.config.proxy_ip = "http://127.0.0.1:" + self.config.pos_agent_port;
                }
            }
        });
    },
});
