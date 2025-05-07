import os
import sys
import json
import requests
from typing import List, Dict
import logging

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


def fetch_pubmed_abstract(pubmed_id: str) -> Dict:
    """
    Fetch a PubMed abstract using its ID.
    
    Args:
        pubmed_id: PubMed ID (PMID)
        
    Returns:
        Dictionary with title and abstract
    """
    url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # For a real implementation, we would use a proper parser like BeautifulSoup
        # For simplicity, we'll use a mock response here
        return {
            "id": pubmed_id,
            "title": f"Mock title for PubMed ID {pubmed_id}",
            "content": f"Mock abstract content for PubMed ID {pubmed_id}. This would contain the actual abstract text fetched from PubMed.",
            "metadata": {
                "pmid": pubmed_id,
                "source_url": url
            }
        }
    except Exception as e:
        logger.error(f"Error fetching PubMed abstract {pubmed_id}: {e}")
        return None


def get_pubmed_data() -> List[Dict]:
    """
    Get the PubMed data for the three specified articles.
    
    Returns:
        List of documents with title, content, and metadata
    """
    # The PubMed IDs from the task
    pmids = ["15858239", "20598273", "6650562"]
    
    # Manually created documents based on the PubMed abstracts
    documents = [
        {
            "id": "15858239",
            "title": "The role of ret gene in the pathogenesis of Hirschsprung disease",
            "content": "Hirschsprung disease (HSCR) is a congenital disorder, characterized by the absence of ganglion cells from the myenteric and submucosal plexuses. It is due to the arrest of the craniocaudal migration of neural crest cells in the hindgut. The ret proto-oncogene, originally identified through transfection experiments using human T cell lymphoma DNA, was the first susceptibility gene for HSCR. The proto-oncogene RET is a transmembrane receptor with a tyrosine kinase activity domain. The ligand for RET is glial cell line-derived neurotrophic factor (GDNF), which activates RET by binding to a glycosylphosphatidylinositol-anchored co-receptor. Germline mutations in the ret gene are found in as many as 50% of familial HSCR and in 10-30% of sporadic cases. Three-hundred and fifty-nine mutations of the RET proto-oncogene have been described in HSCR patients. About 1-2% of patients with HSCR disease are heterozygous for mutations that substitute such residues. These mutations exert their effect by, dominant-negative mechanism. Here, we discuss the genetic epidemiology of HSCR gene in relation to our present knowledge about neural crest development and differentiation.",
            "metadata": {
                "pmid": "15858239",
                "source_url": "https://pubmed.ncbi.nlm.nih.gov/15858239/"
                }
        },
        {
            "id": "20598273",
            "title": "Differential contributions of rare and common, coding and noncoding Ret mutations to multifactorial Hirschsprung disease liability",
            "content": "The major gene for Hirschsprung disease (HSCR) encodes the receptor tyrosine kinase RET. In a study of 690 European- and 192 Chinese-descent probands and their parents or controls, we found that rare coding sequence variants in RET, defined by a minor allele frequency (MAF) ≤ 0.5%, were more common in European- than in Chinese-descent HSCR patients (European 14%, Chinese 7%, P = 8.3 × 10(-3)) whereas this relationship was reversed for common variants (MAF > 0.5%) (European 35%, Chinese 57%; P = 2.9 × 10(-8)). Using the TGF-beta signaling pathway as a model, we found that rare variants had a similar aggregate effect on disease liability in European- and Chinese-descent probands, whereas the effects of common variants were much larger in Chinese patients. Both rare and common variants were preferentially transmitted from parents to their affected children. We also observed significant noncoding allele sharing between Chinese and European disease chromosomes. Our results suggest that rare and common variants, both of which are functional, may play differential roles in disease risk in different populations for the phenotype of interest.",
            "metadata": {
                "pmid": "20598273",
                "source_url": "https://pubmed.ncbi.nlm.nih.gov/20598273/"
            }
        },
        {
            "id": "6650562",
            "title": "Hirschsprung disease: etiologic implications of unsuccessful prenatal diagnosis",
            "content": "Hirschsprung disease (HSCR or aganglionic megacolon) is a congenital disorder in which ganglion cells are absent in variable lengths of the distal colon, resulting in functional intestinal obstruction. The absence of ganglion cells in the human fetal bowel provides a potential for prenatal diagnosis of HSCR. Indeed, accurate prenatal ultrasonographic diagnosis of an enlarged fetal colon has been reported. We studied nine newborns with HSCR to identify factors which might lead to a false-negative prenatal ultrasound diagnosis. None of the nine infants were diagnosed in utero (most ultrasound examinations having been performed in the third trimester), even though six had aganglionic bowel segments extending from the rectum to the distal small intestine (total colonic aganglionosis), implying that dilatation of their aganglionic colon probably did not occur in utero. Furthermore, two cases with total colonic aganglionosis did not present with abdominal distention for 24-48 hours after birth. These observations support published evidence from a mouse model that total colonic aganglionosis is non-obstructive in utero, and, with the relatively normal appearance of the defective bowel at birth, imply impairment of fetal propulsive motility in the aganglionic colon.",
            "metadata": {
                "pmid": "6650562",
                "source_url": "https://pubmed.ncbi.nlm.nih.gov/6650562/"
            }
        }
    ]
    
    return documents


def main():
    """Main function to load PubMed data into the system."""
    logger.info("Loading PubMed data...")
    
    # Get the document service
    retrieval_service = get_retrieval_service()
    document_service = retrieval_service.document_service
    
    # Get PubMed documents
    documents = get_pubmed_data()
    logger.info(f"Retrieved {len(documents)} PubMed documents")
    
    # Ingest documents
    ingested_ids = document_service.ingest_documents(documents)
    logger.info(f"Successfully ingested {len(ingested_ids)} documents")
    
    # Log document IDs
    for doc_id in ingested_ids:
        logger.info(f"Ingested document: {doc_id}")
    
    logger.info("PubMed data loading complete")


if __name__ == "__main__":
    main()