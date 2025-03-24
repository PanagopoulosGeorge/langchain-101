
###  Automating RTEC Prompting

An attempt for automating the prompting process of LLMs for RTEC rule generation.

#### Project Overview

This project aims to automate the process of interacting with LLMs using structured prompts in the RTEC format. 
Given a document containing a series of structured prompts, that are categorized in the following section, the main task is to programmatically prompt this series of prompts to multiple LLMs for generating responses, extracting the answers and validate them using a prolog file acting as the ground truth. There is already a framework for comparing test results, so the process of validating is out of the scope of this project.
The system handles both training prompts and testing prompts for maritime situational awareness (MSA) scenarios.

-   Maritime Situational Awareness (MSA)

#### Prompt Categories

*  **General Training Prompts**: RTEC-1 through RTEC-SDF2

	* Contains basic RTEC syntax and conventions.

*  **Contect Specific Prompts**: Prompt MSA through Prompt MSA-BK
	* Contains domain specific knowledge

*  **Testing Prompts**: Prompt MSA-R1 Through Prompt MSA-R18
	* These prompts will be used to assess the models learning process.

### Goal of the learning process

1.  **Input Processing**
    
    -   Accept natural language descriptions of composite activities
    -   Process predefined events and fluents for each domain
    -   Handle background knowledge predicates

2.  **Rule Generation**
    
    -   Generate valid RTEC rules in Prolog syntax
    -   Support two types of rule definitions:
        -   Simple fluent definitions (using initiatedAt/terminatedAt)
        -   Statically determined fluent definitions (using holdsFor)
      
3.  **Domain Support**

	-   Handle 12 predefined events (e.g., change_in_speed_start, gap_start)
	-   Process input fluents (e.g., proximity)
	-   Use 15 background knowledge predicates (e.g., thresholds, vesselType)

#### Technical Constraints

1.  **Rule Format**
    
    -   Follow Prolog conventions
    -   Variables start with uppercase
    -   Predicates and constants start with lowercase
    -   Rules end with full-stop
    -   Head separated from body with ":-"

#### MVP Deliverables

1.  **Core System**
    
    -   Prompt processing module
    -   Rule generation engine

2.  **Domain Implementation**
    
    -   Support for MSA rules
    -   Background knowledge integration

3.  **Documentation**
    
    -   System architecture
    -   Usage guidelines
    -   Example implementations