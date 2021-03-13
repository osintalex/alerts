from app.alerts import Alerts
from app.utilities import listings
import logging

Alerts = Alerts()


def main():
    for item in listings:
        output = Alerts.get_listing(listing=item)
        results = Alerts.check_for_updates(new_listing=output, listing=item)
        if results:
            Alerts.send_email(listing=results)


if __name__ == "__main__":
    logging.basicConfig(filename='alerts.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(message)s')
    main()
