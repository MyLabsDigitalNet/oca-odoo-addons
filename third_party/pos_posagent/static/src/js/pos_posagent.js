odoo.define('pos_posagent.pos_posagent', function (require) {
    "use strict";
    var { PosGlobalState } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const PosAgentPosGlobalState = (PosGlobalState) => class PosAgentPosGlobalState extends PosGlobalState {
        after_load_server_data() {
            var self = this;
            return super.after_load_server_data(...arguments).then(function () {
                if (self.config.posagent_enable_printer) self.config.iface_print_via_proxy = true;
                if (self.config.posagent_enable_cash_drawer) self.config.iface_cashdrawer = true;
                if (self.config.use_posagent && (self.config.posagent_enable_printer)) {
                    self.config.use_proxy = true;
                    if (self.config.posagent_enable_printer) self.config.iface_print_via_proxy = true;
                    if (self.config.posagent_enable_cashdrawer) self.config.iface_cashdrawer = true;
                    self.config.iface_customer_facing_display_via_proxy = false;
                    self.config.iface_scan_via_proxy = false;
                    self.config.iface_electronic_scale = false;
                    self.config.proxy_ip = "http://127.0.0.1:" + self.config.pos_agent_port;
                }
            });
        }
    }


    Registries.Model.extend(PosGlobalState, PosAgentPosGlobalState);
});
