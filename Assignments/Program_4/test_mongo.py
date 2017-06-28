from pymongo import MongoClient

class MongoHelper(object):
    def __init__(self):
        self.db_airports = MongoClient().tugtutorial.airports
        self.db_states = MongoClient().tugtutorial.states


    def get_all_airports(self, type="International"):
        all_airports = self.db_airports.find({"type":type})
        results = []
        for ap in all_airports:
            results.append(ap)

        return results

    
    def get_doc_by_keyword(self, field, key):
        result = self.db_airports.find({field:{'$regex':'.*'+key+'.*'}})

        res_list = []

        for r in result:
            res_list.append(r)

        return res_list

    def get_stat
        
if __name__ == "__main__":

    mh = MongoHelper
    #gaa = mh.get_all_airports("International")
    #print(gaa)

    county_stuff = mh.get_doc_by_keyword("name", "county")
    print(county_stuff)
