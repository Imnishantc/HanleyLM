class ReportGenerator:

    def __init__(self):

        self.results = []

        self.findings = []

        self.summary = None

    def load_results(self):

        pass

    def build_findings(self):

        pass

    def build_summary(self):

        pass

    def generate_pdf(self):

        pass

    def generate_reports(self):

        self.load_results()

        self.build_findings()

        self.build_summary()

        self.generate_pdf()