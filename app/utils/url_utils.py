from urllib.parse import urlparse

def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    domain_parts = domain.replace("www.", "").split('.')
    essential_domain_part = domain_parts[0] if domain_parts else domain
    return essential_domain_part
