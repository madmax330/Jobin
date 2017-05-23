

class ExtendedEvent:

    def __init__(self, event, company, interested):
        self.pk = event.pk
        self.name = company.name
        self.cweb = company.website
        self.caddr = company.address + ', ' + company.city + ', ' + company.state + ', ' + company.zipcode
        self.logo = company.logo
        self.title = event.title
        self.address = event.address + ', ' + event.city + ', ' + event.state + ', ' + event.zipcode
        self.start_date = event.start_date
        self.start_time = event.start_time
        self.website = event.website
        self.desc = event.description
        self.interested = interested



