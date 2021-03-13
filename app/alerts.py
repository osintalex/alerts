import requests
from dataclasses import dataclass
import pickle
import logging
from app.credentials import credentials
import smtplib
import ssl
import os
from .config import project_root


@dataclass
class Alerts:
    sender_email: str = credentials["sender_email"]
    receiver_email: str = credentials["receiver_email"]
    password: str = credentials["password"]

    @staticmethod
    def get_listing(listing):
        """
        :param listing: tuple, listing name, listing url.
        Sends a GET request to a particular job listing page.
        :return: response.content, response from the listings page.
        """

        # Make request
        response = requests.get(listing[1])
        if response.status_code == 200:
            return response.content
        else:
            logging.info(
                "Did not receive a response from the server for listing {}".format(
                    listing
                )
            )
            logging.info(
                "Response status code {}".format(response.status_code, response.reason)
            )
            raise Exception

    @staticmethod
    def check_for_updates(new_listing, listing):
        """
        :param new_listing: response.content object, the response from the server about the listing's current state.
        :param listing: tuple, listing name, listing url.
        Checks if the listing page has changed.
        :return listing: string, url for the new listing.
        """

        # Check if this is a new listing, if so write to file
        listings_dir = os.path.join(project_root, "app/listings")
        all_listings = [x for x in os.walk(listings_dir)][0]
        if [listing[0]] not in all_listings:
            logging.info("New listing discovered - writing {} to file".format(listing))
            with open(listings_dir + "/" + listing[0], "wb") as f:
                pickle.dump(new_listing, f)
            return listing

        # Open the file
        with open(listings_dir + "/" + listing[0], "rb") as f:
            old_listing = pickle.load(f)

        if old_listing == new_listing:
            logging.info("No new information discovered for listing {}".format(listing))
        else:
            logging.info("New information discovered for listing {}".format(listing))
            # Write new listing information to file for future comparisons
            with open(listings_dir + "/" + listing[0], "wb") as f:
                pickle.dump(new_listing, f)
            return listing

    @classmethod
    def send_email(cls, listing):
        """
        Sends me an email alert if there is a new listing.
        :param listing: tuple, listing name, listing url.
        return sent: dictionary, normally empty unless anything goes wrong - included for testing purposes.
        """
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls

        # Create a secure SSL context
        context = ssl.create_default_context()
        message = "Subject: {}\n\n{}".format(listing[0], listing[1])
        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(cls.sender_email, cls.password)
            sent = server.sendmail(cls.sender_email, cls.receiver_email, message)
            logging.info("This was the message sent {}".format(message))
            return sent
        except Exception as e:
            logging.info(e)
        finally:
            server.quit()
