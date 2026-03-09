import streamlit as st
import json
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Betty Ingestion Assistant", layout="wide")

# Title and description
st.title("🎯 Betty Ingestion Assistant")
st.markdown("Streamline client onboarding with intelligent content ingestion recommendations")

# Initialize session state for form persistence
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Create two-column layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("Client Information")
    
    # Basic client info
    client_name = st.text_input("Client Name", placeholder="Enter client name")
    website = st.text_input("Website", placeholder="https://example.com")
    
    st.header("Content & Platform Details")
    
    # CMS Selection
    cms = st.selectbox(
        "CMS Platform",
        ["WordPress", "Drupal", "Sitefinity", "DNN", "Umbraco", "Storyblok", "Other", "Unknown"]
    )
    
    st.header("Content Access")
    
    # Content access questions
    public_content = st.radio("Public content only?", ["Yes", "No"], horizontal=True)
    member_content = st.radio("Member or gated content?", ["Yes", "No"], horizontal=True)
    content_login = st.radio("Content behind login?", ["Yes", "No"], horizontal=True)
    separate_instances = st.radio("Need separate public and member instances?", ["Yes", "No"], horizontal=True)
    
    st.header("Ingestion Preferences")
    
    # Preferred method
    preferred_method = st.selectbox(
        "Preferred ingestion method?",
        ["API", "RSS", "Crawler", "Unsure"]
    )

with col2:
    st.header("Content Types")
    
    # Content types multi-select
    content_types = st.multiselect(
        "What content types need ingestion?",
        [
            "HTML pages",
            "PDFs",
            "White Papers",
            "Case Studies",
            "Marketplace",
            "Journals",
            "Podcasts",
            "Webinars",
            "Videos",
            "YouTube",
            "RSS Feeds",
            "Ebooks"
        ]
    )
    
    st.header("Content Quality & Format")
    
    # PDF and video/audio details
    if "PDFs" in content_types or "White Papers" in content_types or "Case Studies" in content_types or "Ebooks" in content_types:
        pdf_text_based = st.radio(
            "Are PDFs text-based?",
            ["Yes", "No", "Unknown"],
            horizontal=True
        )
    else:
        pdf_text_based = None
    
    if "Podcasts" in content_types or "Webinars" in content_types or "Videos" in content_types or "YouTube" in content_types:
        transcripts_available = st.radio(
            "Are transcripts available for video or audio content?",
            ["Yes", "No", "Unknown"],
            horizontal=True
        )
    else:
        transcripts_available = None
    
    st.header("Additional Context")
    
    # Additional notes
    additional_notes = st.text_area(
        "Additional notes or special requirements",
        placeholder="Enter any additional information...",
        height=150
    )

# Generate recommendations button
if st.button("🚀 Generate Recommendation", use_container_width=True, type="primary"):
    st.session_state.submitted = True

# Display results if submitted
if st.session_state.submitted:
    st.divider()
    
    # Collect all form data
    form_data = {
        "client_name": client_name,
        "website": website,
        "cms": cms,
        "public_content": public_content,
        "member_content": member_content,
        "content_login": content_login,
        "separate_instances": separate_instances,
        "preferred_method": preferred_method,
        "content_types": content_types,
        "pdf_text_based": pdf_text_based,
        "transcripts_available": transcripts_available,
        "additional_notes": additional_notes
    }
    
    # Generate recommendations based on business logic
    recommendation = generate_strategy(form_data)
    secondary_method = generate_secondary_method(form_data)
    deliverables = generate_deliverables(form_data)
    risks = generate_risks(form_data)
    next_steps = generate_next_steps(form_data)
    internal_notes = generate_internal_notes(form_data)
    draft_email = generate_draft_email(form_data)
    
    # Display in tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Strategy",
        "Secondary Method",
        "Deliverables",
        "Risks & Blockers",
        "Next Steps",
        "Internal Notes",
        "Draft Email"
    ])
    
    with tab1:
        st.subheader("Recommended Ingestion Strategy")
        st.markdown(recommendation)
    
    with tab2:
        st.subheader("Secondary / Backup Method")
        st.markdown(secondary_method)
    
    with tab3:
        st.subheader("Required Client Deliverables")
        st.markdown(deliverables)
    
    with tab4:
        st.subheader("Risks or Blockers")
        st.markdown(risks)
    
    with tab5:
        st.subheader("Next Steps")
        st.markdown(next_steps)
    
    with tab6:
        st.subheader("Internal Notes")
        st.markdown(internal_notes)
    
    with tab7:
        st.subheader("Draft Client Email")
        st.markdown(draft_email)
    
    # Export button
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        json_export = json.dumps(form_data, indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=json_export,
            file_name=f"ingestion_{client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    with col2:
        # Create markdown export
        markdown_export = f"""# Ingestion Recommendation - {client_name}\n\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n## Recommended Strategy\n{recommendation}\n\n## Secondary Method\n{secondary_method}\n\n## Deliverables\n{deliverables}\n\n## Risks & Blockers\n{risks}\n\n## Next Steps\n{next_steps}\n\n## Internal Notes\n{internal_notes}\n\n## Draft Client Email\n{draft_email}\n"""
        st.download_button(
            label="📄 Download as Markdown",
            data=markdown_export,
            file_name=f"ingestion_{client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )


# Business logic functions
def generate_strategy(data):
    """Generate primary ingestion strategy based on inputs"""
    cms = data["cms"]
    preferred = data["preferred_method"]
    content_types = data["content_types"]
    
    api_first_cms = ["WordPress", "Drupal", "Sitefinity", "DNN", "Umbraco", "Storyblok"]
    
    strategy = ""
    
    if cms in api_first_cms:
        strategy += f"**Primary Method: API Integration**\n\n"
        strategy += f"The {cms} platform supports native API capabilities, making API integration the optimal approach for {data['client_name']}.*\n\n"
        strategy += "**Benefits:**\n"
        strategy += "- Real-time content synchronization\n"
        strategy += "- Structured data extraction\n"
        strategy += "- Automated updates and scalability\n"
    elif preferred == "API":
        strategy += f"**Primary Method: API Integration**\n\n"
        strategy += f"Based on your preference and {data['client_name']}'s platform, API integration is recommended.*\n\n"
    elif preferred == "RSS" or "RSS Feeds" in content_types:
        strategy += f"**Primary Method: RSS Feed Ingestion**\n\n"
        strategy += f"RSS feeds provide an efficient method for content syndication to Betty.*\n\n"
    else:
        strategy += f"**Primary Method: Web Crawler**\n\n"
        strategy += f"A web crawler will systematically index content from {data['client_name']}'s website.*\n\n"
    
    # Add content-specific notes
    if "YouTube" in content_types:
        strategy += f"\n**YouTube Content:**\n"
        strategy += f"- YouTube playlist ingestion will be configured\n"
        strategy += f"- Captions and transcripts are required for optimal indexing\n"
    
    if "PDFs" in content_types or "White Papers" in content_types or "Case Studies" in content_types or "Ebooks" in content_types:
        strategy += f"\n**Document Ingestion (PDFs, White Papers, Case Studies, Ebooks):**\n"
        if data["pdf_text_based"] == "Yes":
            strategy += f"- Text-based PDFs confirmed - direct ingestion recommended\n"
        elif data["pdf_text_based"] == "No":
            strategy += f"- PDFs require OCR or text conversion before ingestion\n"
        else:
            strategy += f"- PDF format verification needed during implementation phase\n"
        strategy += f"- Consider SFTP for large-scale document drops\n"
    
    if data["member_content"] == "Yes" or data["content_login"] == "Yes":
        strategy += f"\n**Authenticated Content:**\n"
        strategy += f"- Login credentials or API tokens required for member-only content\n"
        strategy += f"- Separate crawl configuration for gated sections\n"
    
    if data["separate_instances"] == "Yes":
        strategy += f"\n**Multi-Instance Setup:**\n"
        strategy += f"- Two separate Betty instances will be configured:\n"
        strategy += f"  1. Public content instance\n"
        strategy += f"  2. Member/gated content instance\n"
    
    return strategy


def generate_secondary_method(data):
    """Generate secondary/backup ingestion method"""
    cms = data["cms"]
    preferred = data["preferred_method"]
    content_types = data["content_types"]
    
    secondary = ""
    
    if cms in ["WordPress", "Drupal", "Sitefinity", "DNN", "Umbraco", "Storyblok"]:
        if "RSS Feeds" in content_types or preferred == "RSS":
            secondary += f"**Secondary Method: RSS Feed Ingestion**\n\n"
            secondary += f"If API access becomes unavailable, RSS feeds can serve as a reliable backup.\n\n"
            secondary += "**Advantages:**\n"
            secondary += "- Independent of API changes\n"
            secondary += "- Widely supported across most CMS platforms\n"
            secondary += "- Minimal setup required\n"
        else:
            secondary += f"**Secondary Method: Web Crawler**\n\n"
            secondary += f"If API integration encounters obstacles, web crawling provides a robust fallback.\n\n"
            secondary += "**Advantages:**\n"
            secondary += "- Works without API documentation\n"
            secondary += "- Captures rendered HTML content\n"
            secondary += "- No authentication required for public content\n"
    else:
        secondary += f"**Secondary Method: Web Crawler**\n\n"
        secondary += f"Web crawling serves as the backup for initial ingestion and ongoing content updates.\n\n"
        secondary += "**Setup:**\n"
        secondary += f"- Crawl pattern configuration for {data['client_name']}'s site structure\n"
        secondary += f"- Update frequency: Based on content publishing cadence\n"
    
    return secondary


def generate_deliverables(data):
    """Generate required client deliverables"""
    deliverables = "**Required from Client:**\n\n"
    
    deliverables += "1. **Access & Credentials**\n"
    deliverables += "   - CMS admin access or API credentials\n"
    
    if data["member_content"] == "Yes" or data["content_login"] == "Yes":
        deliverables += "   - Login credentials for gated/member content areas\n"
        deliverables += "   - Test user accounts for authentication testing\n"
    
    deliverables += "\n2. **Technical Documentation**\n"
    deliverables += "   - Site map or URL structure documentation\n"
    
    if data["cms"] not in ["Unknown", "Other"]:
        deliverables += f"   - {data['cms']} API documentation (if using API)\n"
    
    if "PDFs" in data["content_types"] or "White Papers" in data["content_types"] or "Case Studies" in data["content_types"] or "Ebooks" in data["content_types"]:
        deliverables += "   - Sample PDFs for format testing\n"
        if data["pdf_text_based"] is None:
            deliverables += "   - Confirmation of PDF text-based format (OCR capable or native text)\n"
    
    if "YouTube" in data["content_types"]:
        deliverables += "   - YouTube channel or playlist IDs\n"
        deliverables += "   - Confirmation of captions/transcripts availability\n"
    
    if "Podcasts" in data["content_types"] or "Webinars" in data["content_types"]:
        deliverables += f"   - Podcast feed URLs or hosting platform details\n"
        if data["transcripts_available"] is None:
            deliverables += "   - Status of transcript availability\n"
    
    deliverables += "\n3. **Content Strategy**\n"
    deliverables += "   - List of content types to ingest (scope document)\n"
    deliverables += "   - Content update frequency expectations\n"
    deliverables += "   - Any content exclusions or restrictions\n"
    
    deliverables += "\n4. **Infrastructure (if applicable)**\n"
    if any(doc_type in data["content_types"] for doc_type in ["PDFs", "White Papers", "Case Studies", "Ebooks"]):
        deliverables += "   - SFTP access for document drops (if applicable)\n"
    
    deliverables += "   - IP whitelist information (if required by client)\n"
    
    return deliverables


def generate_risks(data):
    """Generate risk assessment and blockers"""
    risks = ""
    has_risks = False
    
    if data["pdf_text_based"] == "No":
        risks += "🚨 **BLOCKER: Non-Text-Based PDFs**\n"
        risks += "   - PDFs require OCR processing or conversion to text-based format\n"
        risks += "   - Increases processing time and may impact accuracy\n"
        risks += "   - Recommend requesting text-based versions from client\n\n"
        has_risks = True
    
    if data["transcripts_available"] == "No" and any(audio_video in data["content_types"] for audio_video in ["Podcasts", "Webinars", "Videos", "YouTube"]):
        risks += "🚨 **BLOCKER: Missing Transcripts**\n"
        risks += "   - Audio/video content without transcripts cannot be effectively indexed\n"
        risks += "   - Recommend implementing transcript generation (manual or automated)\n"
        risks += "   - Consider services like Rev.com or automated captioning tools\n\n"
        has_risks = True
    
    if data["cms"] == "Unknown":
        risks += "⚠️ **Risk: Unknown CMS Platform**\n"
        risks += "   - Requires platform investigation before ingestion configuration\n"
        risks += "   - May impact API availability and integration approach\n\n"
        has_risks = True
    
    if data["content_login"] == "Yes" and not data.get("additional_notes", "").strip():
        risks += "⚠️ **Risk: Login-Protected Content Complexity**\n"
        risks += "   - Requires authenticated access for indexing\n"
        risks += "   - May need additional security considerations\n\n"
        has_risks = True
    
    if data["preferred_method"] == "Unsure" and data["cms"] == "Unknown":
        risks += "⚠️ **Risk: Ingestion Method Uncertainty**\n"
        risks += "   - Requires discovery call to finalize approach\n"
        risks += "   - May delay implementation timeline\n\n"
        has_risks = True
    
    if not has_risks:
        risks += "✅ **No major risks identified.** Proceed with standard onboarding.\n"
    
    return risks


def generate_next_steps(data):
    """Generate action items for next steps"""
    steps = "1. **Initial Consultation Call**\n"
    steps += f"   - Schedule 30-min call with {data['client_name']}\n"
    steps += "   - Confirm technical details and access requirements\n"
    steps += "   - Review and finalize this ingestion plan\n\n"
    
    steps += "2. **Credential & Access Setup**\n"
    if data["cms"] not in ["Unknown", "Other"]:
        steps += f"   - Request {data['cms']} API credentials or CMS admin access\n"
    steps += "   - Test access and document authentication method\n\n"
    
    steps += "3. **Content Scope Finalization**\n"
    steps += "   - Provide client with detailed content type requirements\n"
    steps += "   - Get sign-off on ingestion approach and timeline\n\n"
    
    steps += "4. **Configuration & Testing**\n"
    if data["separate_instances"] == "Yes":
        steps += "   - Provision two Betty instances (public + member)\n"
    else:
        steps += "   - Provision Betty instance with agreed configuration\n"
    
    if data["cms"] in ["WordPress", "Drupal", "Sitefinity", "DNN", "Umbraco", "Storyblok"]:
        steps += f"   - Configure {data['cms']} integration\n"
    
    steps += "   - Conduct test ingestion with sample content\n"
    steps += "   - Validate content quality and completeness\n\n"
    
    steps += "5. **Client Training & Launch**\n"
    steps += "   - Provide client documentation on Betty usage\n"
    steps += "   - Conduct hands-on training session\n"
    steps += "   - Go live with full content ingestion\n\n"
    
    steps += "6. **Monitoring & Optimization**\n"
    steps += "   - Monitor ingestion health for first 30 days\n"
    steps += "   - Collect feedback and optimize as needed\n"
    steps += "   - Schedule quarterly review for ongoing maintenance\n"
    
    return steps


def generate_internal_notes(data):
    """Generate internal implementation notes"""
    notes = ""
    
    cms = data["cms"]
    if cms in ["WordPress", "Drupal", "Sitefinity", "DNN", "Umbraco", "Storyblok"]:
        notes += f"**CMS:** {cms} - Native API preferred\n"
    elif cms == "Unknown":
        notes += f"**CMS:** UNKNOWN - Requires discovery\n"
    else:
        notes += f"**CMS:** {cms}\n"
    
    notes += f"**Ingestion Method:** "
    if data["preferred_method"] != "Unsure":
        notes += f"{data['preferred_method']}\n"
    else:
        notes += "TBD - depends on CMS capabilities\n"
    
    if data["separate_instances"] == "Yes":
        notes += f"**Setup:** Dual instances (public + member)\n"
    else:
        notes += f"**Setup:** Single instance\n"
    
    notes += f"**Content Types:** {', '.join(data['content_types']) if data['content_types'] else 'Not specified'}\n"
    
    if data["pdf_text_based"] is not None:
        notes += f"**PDF Status:** {data['pdf_text_based']}\n"
    
    if data["transcripts_available"] is not None:
        notes += f"**Transcripts:** {data['transcripts_available']}\n"
    
    if data["additional_notes"]:
        notes += f"\n**Notes:** {data['additional_notes']}\n"
    
    return notes


def generate_draft_email(data):
    """Generate professional draft client email"""
    client_name = data["client_name"].split()[0] if data["client_name"] else "Valued Partner"
    
    email = f"""Dear {client_name},\n\nThank you for providing the detailed information about your content ingestion needs. We're excited to partner with you on bringing your content into Betty!\n\nBased on our review, we've developed a tailored ingestion strategy specifically for your organization:\n\n**Our Recommended Approach:**\n\nWe recommend a **{generate_strategy(data).split('**')[1].split('**')[0]}** integration for your content. This approach will enable seamless, real-time content synchronization while maintaining the highest standards for content quality and accessibility.\n\n**What This Means for You:**\n\n✓ Automated content updates directly from your platform\n✓ Comprehensive indexing of all {len(data['content_types'])} content types\n✓ Scalable solution as your content grows\n✓ Dedicated support throughout implementation\n\n**Next Steps:**\n\nTo move forward, we'll need to schedule a brief kickoff call to:\n- Confirm technical requirements and API access\n- Finalize the content scope and update frequency\n- Address any specific requirements or constraints\n\n**Your Part:**\n\nWe'll be requesting the following to get started:\n- CMS admin or API credentials\n- Site map or URL structure documentation\n- Any sample content for testing"""
    
    if data["member_content"] == "Yes" or data["content_login"] == "Yes":
        email += "\n- Test accounts for authenticated content areas\n"
    
    if "YouTube" in data["content_types"]:
        email += "\n- YouTube channel/playlist IDs and caption availability confirmation\n"
    
    if "PDFs" in data["content_types"] or "White Papers" in data["content_types"]:
        email += "\n- Confirmation that PDFs are text-based (ready for direct ingestion)\n"
    
    email += f"\n\nWe're committed to making this implementation smooth and successful. Our team will work closely with you to ensure Betty is properly configured and ready to deliver value immediately.\n\nPlease let us know your availability for a 30-minute kickoff call within the next week. We're flexible and happy to work around your schedule.\n\nLooking forward to working together!\n\nBest regards,\n[Your Name]\n[Your Title]\nBetty Ingestion Team"""  
    return email