from app.main import classify_manager as cm



def get_technical_skills(domain, text):
    """
    Use classify_manager to extract skill from text.
    Return: 
        (skills, explanation)
        skills: array.
        explanation: dictionary.
    """

    if domain not in cm.supported_domains:
        print("Request to extract the unsupported domain.")
        raise ValueError("Unsupported domain.")
    
    result_dict = cm.run_classifier(domain=domain, job_description=text, explanation=True).get_dict()
    skills = result_dict['union']
    explanation = result_dict['explanation']
    return (skills, explanation)