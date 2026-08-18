"""
GROOM AI Website Generator

Local website-generation engine.
No Gemini API.
No external AI API.

This first version creates a structured website from
the user's request and is designed to be upgraded
with a local AI model later.
"""

import re


def extract_name(prompt):
    """
    Try to find a website/business name.
    """

    patterns = [
        r'called\s+["\']?([^"\'.\n]+)',
        r'named\s+["\']?([^"\'.\n]+)',
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            prompt,
            re.IGNORECASE
        )

        if match:

            name = match.group(1).strip()

            if name:
                return name

    return "My Website"


def detect_type(prompt):

    text = prompt.lower()

    if any(word in text for word in [
        "restaurant",
        "cafe",
        "food",
        "kitchen"
    ]):
        return "restaurant"

    if any(word in text for word in [
        "portfolio",
        "developer",
        "designer",
        "freelancer"
    ]):
        return "portfolio"

    if any(word in text for word in [
        "gym",
        "fitness",
        "workout"
    ]):
        return "fitness"

    if any(word in text for word in [
        "shop",
        "store",
        "ecommerce",
        "product"
    ]):
        return "store"

    return "business"


def generate_website(prompt):

    name = extract_name(prompt)

    website_type = detect_type(prompt)

    html = generate_html(
        name,
        website_type
    )

    css = generate_css(
        website_type
    )

    js = generate_js()

    return {
        "html": html,
        "css": css,
        "js": js
    }


def generate_html(name, website_type):

    if website_type == "restaurant":

        hero_text = (
            "Fresh food. Beautiful moments."
        )

        service_title = "Our Menu"

    elif website_type == "portfolio":

        hero_text = (
            "Creative work. Powerful ideas."
        )

        service_title = "My Work"

    elif website_type == "fitness":

        hero_text = (
            "Build strength. Build confidence."
        )

        service_title = "Our Programs"

    elif website_type == "store":

        hero_text = (
            "Discover products you'll love."
        )

        service_title = "Featured Products"

    else:

        hero_text = (
            "Build something amazing with us."
        )

        service_title = "What We Offer"


    return f"""
<header class="hero">

    <nav class="navbar">

        <div class="logo">
            {name}
        </div>

        <div class="nav-links">

            <a href="#home">
                Home
            </a>

            <a href="#about">
                About
            </a>

            <a href="#services">
                Services
            </a>

            <a href="#contact">
                Contact
            </a>

        </div>

    </nav>


    <section id="home" class="hero-content">

        <p class="eyebrow">
            Welcome to {name}
        </p>

        <h1>
            {hero_text}
        </h1>

        <p>
            A modern website created with
            GROOM AI.
        </p>

        <a
            href="#contact"
            class="primary-button"
        >
            Get Started
        </a>

    </section>

</header>


<section
    id="about"
    class="section"
>

    <p class="eyebrow">
        About Us
    </p>

    <h2>
        Welcome to {name}
    </h2>

    <p>
        We create meaningful experiences
        for our customers with quality,
        creativity and modern ideas.
    </p>

</section>


<section
    id="services"
    class="section light-section"
>

    <p class="eyebrow">
        Explore
    </p>

    <h2>
        {service_title}
    </h2>


    <div class="cards">

        <div class="card">

            <div class="card-icon">
                ✦
            </div>

            <h3>
                Quality
            </h3>

            <p>
                High-quality experiences
                designed for you.
            </p>

        </div>


        <div class="card">

            <div class="card-icon">
                ◆
            </div>

            <h3>
                Modern
            </h3>

            <p>
                Beautiful modern solutions
                built with care.
            </p>

        </div>


        <div class="card">

            <div class="card-icon">
                ★
            </div>

            <h3>
                Trusted
            </h3>

            <p>
                We focus on delivering
                results our customers love.
            </p>

        </div>

    </div>

</section>


<section
    id="contact"
    class="section contact-section"
>

    <p class="eyebrow">
        Contact
    </p>

    <h2>
        Let's work together
    </h2>

    <p>
        Get in touch with {name}.
    </p>

    <button
        class="primary-button"
        onclick="contactMessage()"
    >
        Contact Us
    </button>

</section>


<footer>

    <strong>
        {name}
    </strong>

    <p>
        Created with GROOM AI
    </p>

</footer>
"""


def generate_css(website_type):

    return """
* {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    margin: 0;
    font-family:
        Arial,
        Helvetica,
        sans-serif;

    color: #171717;
    background: #ffffff;
}

.hero {
    min-height: 650px;

    color: white;

    background:
        linear-gradient(
            135deg,
            #111111,
            #10A37F
        );
}

.navbar {
    max-width: 1100px;

    margin: auto;

    padding: 25px 20px;

    display: flex;

    justify-content:
        space-between;

    align-items: center;
}

.logo {
    font-size: 20px;
    font-weight: bold;
}

.nav-links {
    display: flex;
    gap: 22px;
}

.nav-links a {
    color: white;
    text-decoration: none;
    font-size: 14px;
}

.hero-content {
    max-width: 900px;

    margin: auto;

    padding:
        110px 20px
        80px;

    text-align: center;
}

.eyebrow {
    color: #10A37F;

    font-size: 13px;

    font-weight: bold;

    text-transform:
        uppercase;

    letter-spacing: 2px;
}

.hero .eyebrow {
    color: #b8ffe9;
}

.hero h1 {
    font-size:
        clamp(
            42px,
            8vw,
            76px
        );

    line-height: 1.05;

    margin:
        20px 0;
}

.hero p {
    font-size: 17px;

    color: #dddddd;

    line-height: 1.7;
}

.primary-button {
    display: inline-block;

    margin-top: 20px;

    padding:
        13px 22px;

    border: none;

    border-radius: 8px;

    background: #10A37F;

    color: white;

    text-decoration: none;

    cursor: pointer;

    font-weight: bold;
}

.section {
    max-width: 1100px;

    margin: auto;

    padding:
        90px 20px;

    text-align: center;
}

.section h2 {
    font-size: 42px;

    margin:
        10px 0 20px;
}

.section > p:not(.eyebrow) {
    max-width: 650px;

    margin:
        auto;

    color: #666;

    line-height: 1.7;
}

.light-section {
    max-width: none;

    background: #f5f7f6;
}

.cards {
    max-width: 1000px;

    margin:
        45px auto 0;

    display: grid;

    grid-template-columns:
        repeat(
            3,
            1fr
        );

    gap: 20px;
}

.card {
    background: white;

    padding: 30px;

    border-radius: 15px;

    box-shadow:
        0 8px 30px
        rgba(
            0,
            0,
            0,
            0.08
        );
}

.card-icon {
    font-size: 28px;

    color: #10A37F;
}

.card h3 {
    margin:
        15px 0 10px;
}

.card p {
    color: #777;

    line-height: 1.6;
}

.contact-section {
    min-height: 400px;
}

footer {
    padding:
        35px 20px;

    text-align: center;

    background: #111111;

    color: white;
}

footer p {
    color: #888;
}

@media (
    max-width: 700px
) {

    .nav-links {
        display: none;
    }

    .hero {
        min-height:
            580px;
    }

    .hero-content {
        padding-top:
            90px;
    }

    .section h2 {
        font-size: 32px;
    }

    .cards {
        grid-template-columns:
            1fr;
    }

}
"""


def generate_js():

    return """
function contactMessage() {

    alert(
        "Thanks for contacting us!"
    );

}
"""