import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django

django.setup()
## 모델의 test_api import해옵니다
from processdata.models import test_api
from SPARQLWrapper import SPARQLWrapper, JSON


def sparql_test():
    sparql = SPARQLWrapper(
        "http://hike.cau.ac.kr/bigdata/namespace/datamap-test/sparql"
    )
    sparql.setQuery(
        """
    PREFIX dm: <http://data.datahub.kr/datamap/def/>
    PREFIX schema: <http://schema.org/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>

    SELECT distinct ?datamapName ?url ?datasetCount
    {
        ?datamap a dm:Datamap ;
                schema:mainEntityOfPage ?url ;
                dm:datamapStat ?dmstat ;
                rdfs:label ?datamapName ;
                
                dm:dataset ?dataset . 
        ?dmstat dm:numberOfDataset ?datasetCount .
    }

    """
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print("sparql 성공")
    return results


## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__ == "__main__":
    results = sparql_test()
    for result in results["results"]["bindings"]:
        test_api(
            dmName=result["datamapName"]["value"],
            mainURL=result["url"]["value"],
            dsCount=result["datasetCount"]["value"],
        ).save()
