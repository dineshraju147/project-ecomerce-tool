from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

faq = Route(
    name='faq',
    utterances=[
        # Return policy variations
        "What is your return policy?",
        "How do I return a product?",
        "Can I return an item if I'm not satisfied?",
        "What is the timeframe for returns?",
        "How long do I have to return a product?",
        "Do you accept product returns?",
        "What is the process to return an item?",
        "Can I return faulty or damaged products?",
        "How do I return defective products?",
        "Are refunds available for returned items?",
        "Do I get a refund for defective products?",
        "How long does it take to process a refund?",
        "When will I get my money back after a return?",
        "What is your refund policy?",
        "Do you provide full refunds or store credit?",

        # Payment-related questions
        "What payment methods do you accept?",
        "Can I pay using a credit card?",
        "Do you accept debit cards or net banking?",
        "Is cash on delivery available?",
        "Can I use HDFC credit card for a discount?",
        "Do you offer any discounts for HDFC cardholders?",
        "Are there any ongoing discounts or offers?",
        "How can I apply a promo code or discount?",

        # Order tracking
        "How can I track my order?",
        "Where is my package?",
        "Can I check the status of my delivery?",
        "When will my order arrive?",
        "Is there a way to see shipment tracking details?",

        # General product questions
        "Do you sell genuine products?",
        "Are your products covered by warranty?",
        "What is the warranty policy?",
        "Can I get help with product installation?",
        "How can I contact customer support?",
    ]
)

sql = Route(
    name='sql',
    utterances=[
        # Product queries with discounts and brands
        "I want to buy Nike shoes with a 50% discount.",
        "Are there any Puma shoes on sale?",
        "Do you have Adidas sneakers available?",
        "Show me running shoes under Rs. 3000.",
        "Are there any formal shoes in size 9?",
        "I need casual shoes in size 8.",
        "Find me sports shoes under 2500 rupees.",
        "What is the price of Puma running shoes?",
        "List all Nike shoes available in size 10.",
        "Show me all shoes under Rs. 2000.",
        "Are there any shoes with a discount right now?",
        "I want shoes that cost less than 1500.",
        "Find formal black shoes in size 9.",
        "Do you have red sneakers in size 7?",
        "Are there any white running shoes available?",
        "What is the cheapest running shoe you have?",
        "Show me Nike shoes that are on discount.",
        "Do you stock Adidas shoes with cashback offers?",
        "Find me sneakers for under 3000 rupees.",
        "I want to buy shoes with free shipping.",
    ]
)

router = SemanticRouter(routes=[faq, sql], encoder=encoder, auto_sync="local" )



if __name__ == "__main__":
    print(router("What is your policy on defective product?" ).name)
    print(router("Pink Puma shoes in price range 5000 to 1000").name)
    print(router("what is your return policy" ).name)