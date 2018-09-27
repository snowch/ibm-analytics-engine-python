import sys
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
else:
    string_types = basestring

class Region:
    
    _valid_regions = ['us-south', 'uk-south']
    
    def __init__(self, region):
        assert isinstance(region, string_types), "region parameter must be a string"
        assert region in self._valid_regions, "Invalid region '{}'.  Supported regions: {}.".format(region, self._valid_regions)
        
        self.region = region
            
    def validate_region(self, region):
        if region not in self._valid_regions:
            raise ValueError(
                
            )

    def api_endpoint(self):
        if   self.region == 'us-south': return 'https://api.ng.bluemix.net'
        elif self.region == 'uk-south': return 'https://api.eu-gb.bluemix.net'
     
    def iam_endpoint(self):
        if   self.region == 'us-south': return 'https://iam.ng.bluemix.net'
        elif self.region == 'uk-south': return 'https://iam.ng.bluemix.net'     
        
    def iae_endpoint(self):
        if   self.region == 'us-south': return 'https://api.us-south.ae.cloud.ibm.com'
        elif self.region == 'uk-south': return 'https://api.eu-gb.ae.cloud.ibm.com'     
       
    def rc_endpoint(self):
        if   self.region == 'us-south': return 'https://resource-controller.ng.bluemix.net'
        elif self.region == 'uk-south': return 'https://resource-controller.eu-gb.bluemix.net'     
        
    def rm_endpoint(self):
        if   self.region == 'us-south': return 'https://resource-manager.ng.bluemix.net'
        elif self.region == 'uk-south': return 'https://resource-manager.eu-gb.bluemix.net' 
       
    