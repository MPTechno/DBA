odoo.define('dba_timesheet', function (require) {
    "use strict";

    var core = require('web.core');
    var data = require('web.data');
    var form_common = require('web.form_common');
    var formats = require('web.formats');
    var Model = require('web.DataModel');
    var time = require('web.time');
    var utils = require('web.utils');

    var QWeb = core.qweb;
    var _t = core._t;
    var true_false = false
    setTimeout(function () {
        var WeeklyTimesheet = core.form_custom_registry.get('weekly_timesheet');
        console.log('________________');
        var CustomerWeeklyTimesheet123 = WeeklyTimesheet.extend({
            init: function () {
                this._super.apply(this, arguments);
                this.set({
                    sheets: [],
                    date_from: false,
                    date_to: false,
                });

                this.field_manager.on("field_changed:timesheet_ids", this, this.query_sheets);
                this.field_manager.on("field_changed:date_from", this, function () {
                    this.set({"date_from": time.str_to_date(this.field_manager.get_field_value("date_from"))});
                });
                this.field_manager.on("field_changed:date_to", this, function () {
                    this.set({"date_to": time.str_to_date(this.field_manager.get_field_value("date_to"))});
                });
                this.field_manager.on("field_changed:user_id", this, function () {
                    this.set({"user_id": this.field_manager.get_field_value("user_id")});
                });
                this.on("change:sheets", this, this.update_sheets);
                this.res_o2m_drop = new utils.DropMisordered();
                this.render_drop = new utils.DropMisordered();
                this.description_line = _t("/");

                console.log('======11======true_false==11=======',true_false);
                new Model('res.users').call('search_read',[[['id', '=', this.session.uid]], ['see_create_edit_in_timesheet'] ], {}).done(function(users){
                    if (users[0]){
                        if (users[0]['see_create_edit_in_timesheet']){
                            console.log('======see_create_edit_in_timesheet==========',users[0]['see_create_edit_in_timesheet'])
                            true_false = users[0]['see_create_edit_in_timesheet']
                        }
                    }
                });
                console.log('======22======true_false==11=======',true_false);

            },
            init_add_project: function () {
                console.log('========myyyy====calll 22222init_add_project==22=======',true_false);
                if (this.dfm) {
                    this.dfm.destroy();
                }
                var self = this;
                // this._super.apply(this, arguments);
                this.$(".oe_timesheet_weekly_add_row").show();
                this.dfm = new form_common.DefaultFieldManager(this);
                this.dfm.extend_field_desc({
                    account_id: {
                        relation: 'account.analytic.account',
                    },
                    code7: {
                        relation: "code.seven",
                    },
                    non_code_activity: {
                        relation: "account.analytic.line",
                    },
                });
                var FieldMany2One = core.form_widget_registry.get('many2one');
                var FieldChar = core.form_widget_registry.get('char');
                var attr_dict = ''
                console.log('======before condition======true_false==22=======',true_false);
                if (true_false){
                    attr_dict = {'attrs': {
                        name: "account_id",
                        type: "many2one",
                        modifiers: '{"required": true}',
                    }}
                }else{
                    attr_dict = {'attrs': {
                        name: "account_id",
                        type: "many2one",
                        modifiers: '{"required": true}',
                        options : "{'no_create_edit': True,'no_quick_create':True,'no_create':True}",
                    }}
                }
                this.account_m2o = new FieldMany2One(this.dfm, attr_dict);   
                this.code7_m2o = new FieldMany2One(this.dfm, {
                    attrs: {
                        name: "code7",
                        type: "many2one",
                        placeholder: "Code-7",
                        domain: [],
                        modifiers: '{"required": false}',
                    },
                });
                this.non_code_activity = new FieldChar(this.dfm, {
                    attrs: {
                        name: "non_code_activity",
                        type: "char",
                        placeholder: "Description",
                        domain: [],
                        modifiers: '{"required": false}',
                    },
                });
                this.non_code_activity.prependTo(this.$(".o_add_timesheet_line > div")).then(function () {
                    self.non_code_activity.$el.addClass('oe_edit_only');
                    self.non_code_activity.$el.css('width', '150px');
                });
                this.code7_m2o.prependTo(this.$(".o_add_timesheet_line > div")).then(function () {
                    self.code7_m2o.$el.addClass('oe_edit_only');
                });
                this.account_m2o.prependTo(this.$(".o_add_timesheet_line > div")).then(function () {
                    self.account_m2o.$el.addClass('oe_edit_only');
                });
                this.$(".oe_timesheet_button_add").click(function () {
                    var id = self.account_m2o.get_value();
                    var pid = self.code7_m2o.get_value();
                    var codeid = self.non_code_activity.get_value();
                    if (codeid === false) {
                        codeid = ''
                    }
                    if (id === false) {
                        self.dfm.set({display_invalid_fields: true});
                        return;
                    }

                    var ops = self.generate_o2m_value();
                    var check = true;
                    for (var i = 0; i < ops.length; i++) {
                        if (ops[i].account_id == id && ops[i].code7_id == pid) {
                            check = false;
                        }
                    }
                    if (check) {
                        ops.push(_.extend({}, self.default_get, {
                            name: self.description_line,
                            unit_amount: 0,
                            date: time.date_to_str(self.dates[0]),
                            account_id: id,
                            code7_id: pid,
                            non_code_activity: codeid,
                            id_group : id+'-'+pid,
                        }));
                    }
                    self.set({sheets: ops});
                    self.destroy_content();
                });
            },
           
        });
        core.form_custom_registry.add('weekly_timesheet', CustomerWeeklyTimesheet123);
    }, 100);
});
