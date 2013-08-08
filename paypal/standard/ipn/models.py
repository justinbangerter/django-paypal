#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from paypal.standard.models import PayPalStandardBase
from paypal.standard.ipn.signals import *
import logging


class PayPalIPN(PayPalStandardBase):
    """Logs PayPal IPN interactions."""
    format = u"<IPN: %s %s>"

    class Meta:
        db_table = "paypal_ipn"
        verbose_name = "PayPal IPN"

    def _postback(self):
        """Perform PayPal Postback validation."""
        return urllib2.urlopen(self.get_endpoint(), "cmd=_notify-validate&%s" % self.query).read()

    def _verify_postback(self):
        if self.response != "VERIFIED":
            self.set_flag("Invalid postback. (%s)" % self.response)

    def send_signals(self):
        """Shout for the world to hear whether a txn was successful."""

        # On all conditions, send the default signal.
        #
        # This reduces the need for app modifications
        # in the case of future PayPal API changes.
        #
        # Consumers of this app may now implement
        # listeners without having to create new signals.
        logging.info("Detected ipn signal: " + self.txn_type)
        ipn_signal.send(sender=self)

        # Transaction signals:
        if self.is_transaction():
            logging.info("Detected transaction: " + self.txn_id)
            if self.flag:
                payment_was_flagged.send(sender=self)
            elif self.is_refund():
                payment_was_refunded.send(sender=self)
            elif self.is_reversed():
                payment_was_reversed.send(sender=self)
            elif self.is_subscription_payment():
                subscription_payment.send(sender=self)
            else:
                payment_was_successful.send(sender=self)
        # Recurring payment signals:
        # XXX: Should these be merged with subscriptions?
        elif self.is_recurring():
            logging.info("Detected recurring signal: " + self.recurring_payment_id)
            if self.is_recurring_create():
                recurring_create.send(sender=self)
            elif self.is_recurring_payment():
                recurring_payment.send(sender=self)
            elif self.is_recurring_cancel():
                recurring_cancel.send(sender=self)
            elif self.is_recurring_skipped():
                recurring_skipped.send(sender=self)
            elif self.is_recurring_failed():
                recurring_failed.send(sender=self)
        # Subscription signals:
        else:
            logging.info("Detected subscription signal:")
            if self.is_subscription_cancellation():
                subscription_cancel.send(sender=self)
            elif self.is_subscription_signup():
                subscription_signup.send(sender=self)
            elif self.is_subscription_end_of_term():
                subscription_eot.send(sender=self)
            elif self.is_subscription_modified():
                subscription_modify.send(sender=self)
            elif self.is_subscription_failed():
                subscription_failed.send(sender=self)

