    # Import necessary libraries

import os  # Used for accessing environment variables like our secret OpenAI API key.
from openai import OpenAI
import openai  # Import the OpenAI library to interact with the API
import streamlit as st  # Streamlit library for creating web apps
from datetime import date
import json

#set default name and info, don't have them enter it 
# don't need session state- done
# could potentially download pdf (option), or can look at easy copy and pasting of an output
# start with default values for patients and physician, with option to edit. Put default values for st.text_input (could use random numbers and have chatgpt
# generate list of random names, populate it with random name)
# use tabs in streamlit instead of sidebar
# get templates from doximity
# could make chatbot with advice for practice administrators. Standard chatbot (chatting with chatgpt), teaching aids git hub has updated one in David's git hub
# could you pull over teaching aids on to that? Maybe forget teaching aids b/c it uses sidebar (want to avoid). Code built in system prompt- practice administrator help
# Can go back and forth and get answer you like and formatting you like, then include that in system prompt so that it knows how to format it 

#Put pretend data for phyisician defaults (hid it), dont let them change it
#let them fill out patient stuff, don't put real patient information 
#add edit patient letter/tweak, make conversational

##ctrl c to stop
# Load your OpenAI API key from secrets.toml
api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = api_key

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=api_key)


def ChatGPT(messages):
    # Ensure messages is a list
    if not isinstance(messages, list):
        messages = [messages]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

st.title("ANN LLM Demo- Prior Authorization Help")
st.write("This is for educational purposes only, please do not input real patient information or use in clinical practice.")
# Use st.radio to create tabs
#page = st.radio("Go to:", ["Chat with chatGPT", "Prior authorization help"])

# Initialize response in session_state if not already present

# Initialize response in session_state if not already present

if 'chat_hx' not in st.session_state:
    st.session_state.chat_hx =  {}
if 'response' not in st.session_state:
    st.session_state["response"] = []
if "messages" not in st.session_state: 
    system_context_friend = "You are a helpful nurse with medical knowledge helping a physician compose a prior authorization to obtain insurance approval for a medication or procedure"
    st.session_state["messages"] = [{"role": "system", "content": system_context_friend}]

# Default physician details
physician_name = "Dr. Jane Doe"
physician_phone = "123-456-7890"
physician_fax = "123-456-7891"
physician_npi = "1234567890"
physician_address = "1234 Health St, Wellness City, HC 12345"

today = date.today()

st.title('Patient Details')
patient_name = st.text_input("Enter patient's name", value="Jane Smith")
patient_dob = st.text_input("Enter patient's date of birth", value="01/01/1950")
med_pa = st.text_input("Enter medication or procedure you are trying to get a prior authorization for", value="lecanemab")
diagnosis = st.text_input("Enter patient's diagnosis", value="Alzheimer's disease")
extra_info = st.text_area("Enter any additional information you would like included in the letter here (optional)", value = "Patient has beend diagnosed with Alzheimer's disease, has no history of stroke/TIA or evidence of other forms of dementia, and has a PET showing prescence of beta-amyloid plaques")
if st.button("Compose Initial Prior Authorization"):
    template_medication = f"""

        {today}

        To Whom It May Concern,

        I am writing to request authorization for {med_pa} for my patient, {patient_name}, diagnosed with {diagnosis}. 

        Physician's Information:
        Name: {physician_name}
        Phone: {physician_phone}
        Fax: {physician_fax}
        NPI: {physician_npi}
        Address: {physician_address}

        Patient's Information:
        Name: {patient_name}
        DOB: {patient_dob}

        Based on the patient's condition and the drug criteria requirements listed below, we believe the patient meets all necessary criteria for {med_pa}.

        Drug Criteria Requirements Met:
        - Patient is 50 years of age or older; or If less than 50 years of age, member has a genetic mutation in amyloid precursor protein (APP), presenilin-1 (PSEN1), or presenilin-2 (PSEN2), or other clinical documentation to support early onset AD.
        - Patinet has mild cognitive impairment due to AD or mild AD dementia
        - Patient has objective evidence of cognitive impairment at baseline
        - Patient has one of the following scores at baseline on any of the assessment tools: Clinical Dementia Rating-Global Score (CDR-GS) of 0.5 or 1, or Mini-Mental Status Examination (MMSE) score of 21 - 30, or MOCA score greater than or equal to 16
        - Patient has a positron emission tomography (PET) scan confirming the presence of amyloid pathology or has results from a lumbar puncture confirming the presence of elevated phosphorylated tau (P-tau) protein and/or elevated total tau (T-tau) protein, and reduced beta amyloid-42 (AB42) OR a low AB42/AB40 ratio as determined by the lab assay detected in cerebrospinal fluid (CSF). 
        - Patient has had a brain MRI within one year
        - Patient has had genotype testing for ApoE ε4 status has been performed prior to initiation of treatment
        - Patient doesn' use antithrombotics, or if they do they have been on a stable dose for at least 4 weeks.

        Please consider this letter as a formal request for the prior authorization of the aforementioned medication. Attached are all necessary medical records and documentation supporting this request.

        Thank you for your attention to this matter.

        Sincerely,

        {physician_name}
        """
    
    template_procedure = f"""
To Whom It May Concern,
        I am writing to request authorization for {med_pa} for my patient, {patient_name}, diagnosed with {diagnosis}. 

        Physician's Information:
        Name: {physician_name}
        Phone: {physician_phone}
        Fax: {physician_fax}
        NPI: {physician_npi}
        Address: {physician_address}

        Patient's Information:
        Name: {patient_name}
        DOB: {patient_dob}

        Botulinum toxin injections are medically necessary and indicated in this patient who is disabled by blepharospasm.
        Patient continues to receive benefit from these injections. Injections will need to be repeated every 3-4 months in order to 
        provide continued benefit for the treatment of this patient's condition.

        Sincerely,
        {physician_name}
    """

    user_query = {"role": "system", "content": f"""Generate a prior authorization letter for either a medication or a procedure. If {med_pa} is a medication, 
            generate a medication prior authorization letter, if {med_pa} is a procedure, generate a procedure prior authorization letter. For a medication use the following structure: {template_medication}. 
            The strucutre is an example for the drug Lecanemab, if a separate drug is requested please fill out the template appropriately with that drug's requirements. 
            Please include the drug requirements in a wording that is approrpriate for a doctor sending a letter to an insurance company about their patient. Please assume the patient has 
            met all the requirements for the drug. For a procedure please use the following strucutre : {template_procedure}. The
            structure is an example for a botox procedure with a patient with a diagnosis of blepharospasm. The wording will need to change depending on the diagnosis and procedure requested. Please include procedure reuiqrements that is approrpriate for that specific procedure requested ({med_pa}) 
            Please assume the patient qualifies for the procedure. For either type of letter (one for a medication or one for a procedure) replace today's date with the actual date of today. Please include {extra_info} if provided in the letter where approrpriate, 
            if {extra_info} is blank or n/a, please don't include."""}
    
    st.session_state.messages.append(user_query)
    response_text = ChatGPT(user_query)
    #st.session_state.chat_hx[user_query] = response_text
    st.session_state.messages.append({"role": "assistant", "content":response_text})
    st.session_state.response.append(response_text)

st.title("Edit the prior authorization")
changes = st.text_area("What would you like to change about the letter?")

# Display the current inputs
#st.subheader("Current Patient Details")
#st.write(f"**Name:** {patient_name}")
#st.write(f"**Date of Birth:** {patient_dob}")
#st.write(f"**Medication or Procedure needing a prior authorization:** {med_pa}")
#st.write(f"**Patient Diagnosis:** {diagnosis}")
#st.write(f"**Additional Information:** {extra_info}")


# Update your session state to include the new message for future reference

if st.button("Edit letter"):
    new_message = {"role": "system", "content": f"""Please edit the prior authorization with these requested edits: {changes}"""}
    st.session_state["messages"].append(new_message)
    response_text = ChatGPT(st.session_state["messages"]) 
    st.session_state["messages"].append({"role": "system", "content": response_text})
    st.session_state.response.append(response_text)
    #st.write(response_text)

if st.session_state.response:
    st.subheader("Current Letter")
    st.write(st.session_state.response[-1])
