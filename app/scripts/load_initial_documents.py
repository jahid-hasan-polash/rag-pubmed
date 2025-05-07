import os
import sys
import json
import logging
from typing import List, Dict
import uuid

# Add the parent directory to sys.path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.retrieval_service import RetrievalService
from app.core.dependencies import get_retrieval_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_initial_documents() -> List[Dict]:
    """
    Get the initial set of documents for ingestion into the system.
    
    Returns:
        List of documents with title, content, and metadata
    """
    # Initial document collection about Hirschsprung disease
    documents = [
        {
            "title": "The role of ret gene in the pathogenesis of Hirschsprung disease",
            "content": "Hirschsprung disease is a congenital disorder with the incidence of 1 per 5000 live births, characterized by the absence of intestinal ganglion cells. In the etiology of Hirschsprung disease various genes play a role; these are: RET, EDNRB, GDNF, EDN3 and SOX10, NTN3, ECE1, Mutations in these genes may result in dominant, recessive or multifactorial patterns of inheritance. Diverse models of inheritance, co-existence of numerous genetic disorders and detection of numerous chromosomal aberrations together with involvement of various genes confirm the genetic heterogeneity of Hirschsprung disease. Hirschsprung disease might well serve as a model for many complex disorders in which the search for responsible genes has only just been initiated. It seems that the most important role in its genetic etiology plays the RET gene, which is involved in the etiology of at least four diseases. This review focuses on recent advances of the importance of RET gene in the etiology of Hirschsprung disease.",
            "metadata": {
                "source_url": "https://pubmed.ncbi.nlm.nih.gov/15858239/"
            }
        },
        {
            "title": "Differential contributions of rare and common, coding and noncoding Ret mutations to multifactorial Hirschsprung disease liability",
            "content": "The major gene for Hirschsprung disease (HSCR) encodes the receptor tyrosine kinase RET. In a study of 690 European- and 192 Chinese-descent probands and their parents or controls, we demonstrate the ubiquity of a >4-fold susceptibility from a C-->T allele (rs2435357: p = 3.9 x 10(-43) in European ancestry; p = 1.1 x 10(-21) in Chinese samples) that probably arose once within the intronic RET enhancer MCS+9.7. With in vitro assays, we now show that the T variant disrupts a SOX10 binding site within MCS+9.7 that compromises RET transactivation. The T allele, with a control frequency of 20%-30%/47% and case frequency of 54%-62%/88% in European/Chinese-ancestry individuals, is involved in all forms of HSCR. It is marginally associated with proband gender (p = 0.13) and significantly so with length of aganglionosis (p = 7.6 x 10(-5)) and familiality (p = 6.2 x 10(-4)). The enhancer variant is more frequent in the common forms of male, short-segment, and simplex families whereas multiple, rare, coding mutations are the norm in the less common and more severe forms of female, long-segment, and multiplex families. The T variant also increases penetrance in patients with rare RET coding mutations. Thus, both rare and common mutations, individually and together, make contributions to the risk of HSCR. The distribution of RET variants in diverse HSCR patients suggests a "cellular-recessive" genetic model where both RET alleles' function is compromised. The RET allelic series, and its genotype-phenotype correlations, shows that success in variant identification in complex disorders may strongly depend on which patients are studied.",
            "metadata": {
                "source_url": "https://pubmed.ncbi.nlm.nih.gov/20598273/"
            }
        },
        {
            "title": "Hirschsprung disease: etiologic implications of unsuccessful prenatal diagnosis",
            "content": "We describe an infant with Hirschsprung disease (congenital aganglionosis of the intestine) involving the colon and terminal ileum. Midtrimester prenatal diagnosis of this disorder in this infant was attempted utilizing amniotic fluid disaccharidase analyses, ultrasound, and amniography. Decreased disaccharidase activities in amniotic fluid have been reported previously in association with other forms of intestinal obstruction. At 15 weeks' gestation, normal amniotic fluid disaccharidase levels were obtained. Serial ultrasound evaluations did not indicate any pathology, and the results from amniography were inconclusive. The implication of the normal disaccharidase values is that Hirschsprung disease may in some cases result from degeneration of intestinal ganglia after 16 weeks' gestation rather than from faulty migration of neural crest cells. The inheritance of Hirschsprung disease is generally consistent with sex-modified multifactorial inheritance with a lower threshold of expression in males. The case we report has a family history of three affected first- and second-degree relatives. Autosomal dominance with variable expressivity is a possible explanation in this family.",
            "metadata": {
                "source_url": "https://pubmed.ncbi.nlm.nih.gov/6650562/"
            }
        }
    ]
    
    logger.info(f"Prepared {len(documents)} initial documents for ingestion")
    return documents


def ingest_initial_documents():
    """
    Load initial document set into the system for RAG processing.
    """
    logger.info("Starting document ingestion...")
    
    # Get the retrieval service and document service
    retrieval_service = get_retrieval_service()
    document_service = retrieval_service.document_service
    
    # Get initial documents
    documents = get_initial_documents()
    
    # Ingest documents
    ingested_ids = document_service.ingest_documents(documents)
    logger.info(f"Successfully ingested {len(ingested_ids)} documents")
    
    # Log document IDs
    for doc_id in ingested_ids:
        logger.info(f"Ingested document: {doc_id}")
    
    logger.info("Document ingestion complete")


if __name__ == "__main__":
    ingest_initial_documents()
