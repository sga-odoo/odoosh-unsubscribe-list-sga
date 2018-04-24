from odoo import models, _


class MassMailing(models.Model):
    """ MassMailing models a wave of emails for a mass mailign campaign.
    A mass mailing is an occurence of sending emails. """
    _inherit = 'mail.mass_mailing'

    def unsubscribe_list(self, opt_out_ids, opt_in_ids, contact_id):
        mailing_contact = self.env['mail.mass_mailing.contact'].sudo().browse(contact_id)
        if opt_out_ids:
            mailing_list_names = self.env['mail.mass_mailing.list'].sudo().browse(opt_out_ids).mapped('name')
            mailing_contact.list_ids = [(6, 0, opt_in_ids)]
            message = _('You have unsubscribed %s mailing list.') % ','.join(mailing_list_names)
            mailing_contact.message_post(body=message)
