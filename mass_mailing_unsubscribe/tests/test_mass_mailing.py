# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class TestMassMailing(common.TransactionCase):

    def test_mass_mailing_unsubscribe_list(self):
        MassMailingContacts = self.env['mail.mass_mailing.contact']
        MassMailing = self.env['mail.mass_mailing']
        self.mailing_list_1 = self.env['mail.mass_mailing.list'].create({'name': 'test 1'})
        self.mailing_list_2 = self.env['mail.mass_mailing.list'].create({'name': 'test 2'})
        self.mailing_list_3 = self.env['mail.mass_mailing.list'].create({'name': 'test 3'})
        self.mailing_contact = MassMailingContacts.create({
                                    'name': 'test email 1',
                                    'email': 'test1@email.com',
                                    'list_ids': [(6, 0, [self.mailing_list_1.id, self.mailing_list_2.id, self.mailing_list_3.id])]})
        # create mass mailing record
        self.mass_mailing = MassMailing.create({
            'name': 'test',
            'body_html': 'This is mass mail marketing demo',
            'mailing_model_id': self.env['ir.model']._get('mail.mass_mailing.list').id,
            'mailing_domain': [('list_ids', 'in', self.mailing_list_1.id)]
            })
        self.mass_mailing.put_in_queue()
        res_ids = self.mass_mailing.get_remaining_recipients()
        composer_values = {
            'body': self.mass_mailing.convert_links()[self.mass_mailing.id],
            'subject': self.mass_mailing.name,
            'model': self.mass_mailing.mailing_model_real,
            'email_from': self.mass_mailing.email_from,
            'composition_mode': 'mass_mail',
            'mass_mailing_id': self.mass_mailing.id,
            'mailing_list_ids': [(4, l.id) for l in self.mass_mailing.contact_list_ids],
        }
        composer = self.env['mail.compose.message'].with_context(active_ids=res_ids).create(composer_values)
        composer.send_mail()
        self.assertEqual(len(self.mailing_contact.list_ids), 3, 'incorrect subscription list count, should be equals to 3')

        opt_out_ids = [self.mailing_list_1.id]  # user unsubscribed list
        opt_in_ids = [self.mailing_list_2.id, self.mailing_list_3.id]

        self.mass_mailing.unsubscribe_list(opt_out_ids, opt_in_ids, self.mailing_contact.id)  # unsubscribe to mailing list
        self.assertEqual(len(self.mailing_contact.list_ids), 2, 'user unsubscribed from given list, should be equals to 2')
