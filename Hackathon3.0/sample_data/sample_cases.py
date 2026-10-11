"""Sample Indian court cases with structured intelligence, page texts, and citations.

Provides instant demo capability for hackathon evaluation without needing API keys
or external file downloads, while also supplying data to generate genuine multipage PDFs.
"""

from typing import Dict, Any, List

SAMPLE_CASES: Dict[str, Dict[str, Any]] = {
    "criminal_quashing": {
        "id": "criminal_quashing",
        "title": "Criminal Appeal: Quashing of FIR & Section 482 CrPC",
        "case_name": "Rajesh Sharma & Ors. v. State of Uttar Pradesh & Anr.",
        "court_name": "Supreme Court of India",
        "case_number": "Criminal Appeal No. 1265 of 2017",
        "decision_date": "27 July 2017",
        "bench": "Hon'ble Mr. Justice A.K. Goel, Hon'ble Mr. Justice U.U. Lalit",
        "case_category": "Criminal",
        "document_type": "Judgment",
        "total_pages": 4,
        "parties": [
            {"role": "Petitioner / Appellant", "name": "Rajesh Sharma & Others", "type": "Individual"},
            {"role": "Respondent 1", "name": "State of Uttar Pradesh", "type": "State / Government"},
            {"role": "Respondent 2", "name": "Sneha Sharma (Informant / Complainant)", "type": "Individual"},
            {"role": "Amicus Curiae", "name": "Senior Advocate V. Shekhar", "type": "Legal Counsel"}
        ],
        "provisions": [
            {
                "act_name": "Code of Criminal Procedure, 1973",
                "section_or_article": "Section 482",
                "context": "Invocation of inherent powers of the High Court to prevent abuse of the process of any court and secure the ends of justice.",
                "supporting_quote": "Inherent power under Section 482 of the Code must be exercised to prevent misuse of statutory criminal machinery where allegations are vague and omnibus.",
                "page_number": 2,
                "is_applied": True,
                "application_type": "Applied / Relied Upon"
            },
            {
                "act_name": "Indian Penal Code, 1860",
                "section_or_article": "Section 498-A",
                "context": "Offense of husband or relative of husband subjecting a woman to cruelty.",
                "supporting_quote": "Section 498-A was enacted to protect women from harassment, but mechanical arrests without verification infringe personal liberty.",
                "page_number": 1,
                "is_applied": True,
                "application_type": "Interpreted & Applied"
            },
            {
                "act_name": "Code of Criminal Procedure, 1973",
                "section_or_article": "Section 41-A",
                "context": "Issuance of notice of appearance before police officer in offenses punishable with imprisonment up to 7 years.",
                "supporting_quote": "The mandate of Section 41-A CrPC must be strictly adhered to by police authorities before any coercive step of arrest is taken.",
                "page_number": 3,
                "is_applied": True,
                "application_type": "Mandated / Enforced"
            }
        ],
        "summary": {
            "case_overview": "This criminal appeal before the Supreme Court concerns the rampant misuse of criminal proceedings under Section 498-A of the Indian Penal Code against distant relatives and family members of the husband without specific allegations, and lays down protective safeguards against arbitrary arrests.",
            "background": "The informant lodged an FIR alleging dowry harassment and cruelty against her husband and his extended family members. The appellants approached the High Court under Section 482 CrPC seeking quashing of criminal proceedings, but the High Court dismissed their petition on the ground that factual allegations must be tested during trial.",
            "main_legal_issue": "Whether criminal proceedings against distant relatives containing omnibus and uncorroborated allegations under Section 498-A IPC should be permitted to continue, and what guidelines should govern arrest to prevent harassment of innocent family members?",
            "arguments": {
                "petitioner_arguments": "The appellants argued that distant relatives living in separate residences were roped in merely due to matrimonial rancour, without any specific role or overt act attributed to them. Continued prosecution amounts to harassment and abuse of process.",
                "respondent_arguments": "The State and complainant argued that the allegations disclosed a prima facie case of demand for dowry and harassment, which cannot be stifled at the inception under Section 482 CrPC before recording of evidence."
            },
            "court_reasoning": "The Supreme Court observed that criminal law cannot be weaponized to settle personal scores against all relatives in matrimonial disputes. The Court emphasized that personal liberty under Article 21 cannot be compromised by mechanical arrests, and the inherent jurisdiction under Section 482 CrPC is specifically designed to quash vexatious proceedings where allegations are general and unspecific.",
            "final_order": "The Supreme Court partly allowed the appeal. Criminal proceedings against the distant relatives (appellants 2 to 4) were quashed. The husband was directed to cooperate with the investigation, with explicit direction that no arrest shall be made without complying with Section 41-A CrPC.",
            "important_takeaways": [
                "Criminal proceedings containing vague, omnibus allegations against distant relatives in matrimonial disputes are liable to be quashed under Section 482 CrPC.",
                "Arrest is not mandatory in every criminal case; police officers must satisfy statutory requirements under Section 41 and 41-A CrPC.",
                "Courts must carefully scrutinize allegations to protect innocent family members from unnecessary trauma of prolonged criminal trial.",
                "This is a final judgment conclusively disposing of the appeal regarding the appellants."
            ]
        },
        "evidence_items": [
            {
                "fact": "Inherent jurisdiction under Section 482 CrPC must prevent abuse of process when allegations are omnibus.",
                "quote": "Inherent power under Section 482 of the Code must be exercised to prevent misuse of statutory criminal machinery where allegations are vague and omnibus.",
                "page": 2,
                "section_or_para": "Paragraph 11"
            },
            {
                "fact": "Police authorities are legally bound to follow Section 41-A CrPC prior to making arrests in offenses carrying under 7 years imprisonment.",
                "quote": "The mandate of Section 41-A CrPC must be strictly adhered to by police authorities before any coercive step of arrest is taken.",
                "page": 3,
                "section_or_para": "Paragraph 18"
            },
            {
                "fact": "Criminal proceedings against distant relatives (Appellants 2 to 4) were quashed by the Court.",
                "quote": "The proceedings against Appellants 2 to 4 are hereby quashed, while Appellant 1 shall participate in the investigation under notice.",
                "page": 4,
                "section_or_para": "Paragraph 24 (Operative Order)"
            }
        ],
        "pages_text": {
            1: """IN THE SUPREME COURT OF INDIA
CRIMINAL APPELLATE JURISDICTION
CRIMINAL APPEAL NO. 1265 OF 2017

Rajesh Sharma & Ors.                                ...Appellants
VERSUS
State of Uttar Pradesh & Anr.                       ...Respondents

CORAM:
HON'BLE MR. JUSTICE A.K. GOEL
HON'BLE MR. JUSTICE U.U. LALIT

JUDGMENT
A.K. GOEL, J.

1. The central question arising in this appeal is the need to check unwarranted arrests and curb the misuse of penal provisions in matrimonial conflicts. Section 498-A was enacted to protect women from harassment, but mechanical arrests without verification infringe personal liberty.

2. In the present case, an FIR was registered under Sections 498-A and 323 of the Indian Penal Code, 1860, along with provisions of the Dowry Prohibition Act, 1961, at Police Station Sadar, against the husband and four of his family members, including married sisters and parents residing at separate places.""",
            2: """CRIMINAL APPEAL NO. 1265 OF 2017                                [PAGE 2]

6. The appellants approached the High Court of Judicature at Allahabad invoking Section 482 of the Code of Criminal Procedure, 1973, seeking to quash the summoning order and the criminal proceedings. The High Court, however, dismissed the petition summarily observing that factual issues cannot be decided at the threshold.

11. Having heard learned counsel for the parties and the learned Amicus Curiae, we are of the considered opinion that the approach of the High Court was flawed. Inherent power under Section 482 of the Code must be exercised to prevent misuse of statutory criminal machinery where allegations are vague and omnibus. A clear distinction must be drawn between active offenders and distant relatives roped in solely out of anger and bitterness.""",
            3: """CRIMINAL APPEAL NO. 1265 OF 2017                                [PAGE 3]

14. The tendency of implicating all family members in matrimonial disputes has been repeatedly deprecated by this Court in several decisions including Preeti Gupta v. State of Jharkhand and Arnesh Kumar v. State of Bihar. 

18. In respect of offenses punishable with imprisonment up to seven years, Parliament has enacted safeguards under Sections 41 and 41-A of the Code. The mandate of Section 41-A CrPC must be strictly adhered to by police authorities before any coercive step of arrest is taken. The police officer must satisfy himself on specified parameters regarding necessity of arrest and record reasons in writing.

20. When general allegations are made without attributing any specific overt role or date or circumstance against extended family members, forcing them to undergo trial is an assault on human dignity and judicial efficiency.""",
            4: """CRIMINAL APPEAL NO. 1265 OF 2017                                [PAGE 4]

22. We accordingly issue the following directions:
(i) No automatic arrest shall be made in matrimonial complaints without prior preliminary enquiry by the Designated Officer.
(ii) Where family members reside outside the territorial jurisdiction, personal appearance should not ordinarily be insisted upon.

24. In the result, the appeal is partly allowed. The proceedings against Appellants 2 to 4 are hereby quashed, while Appellant 1 shall participate in the investigation under notice. The order of the High Court is modified in the above terms.

................................................J.
(A.K. GOEL)

................................................J.
(U.U. LALIT)
NEW DELHI;
JULY 27, 2017."""
        }
    },

    "commercial_arbitration": {
        "id": "commercial_arbitration",
        "title": "Commercial Arbitration: Section 9 Interim Measures & Jurisdiction",
        "case_name": "Nexora Infra Private Limited v. Apex Global Energy Corporation",
        "court_name": "High Court of Delhi",
        "case_number": "O.M.P. (I) (COMM.) No. 342 of 2023",
        "decision_date": "14 November 2023",
        "bench": "Hon'ble Mr. Justice Prateek Jalan",
        "case_category": "Commercial",
        "document_type": "Interim Order",
        "total_pages": 3,
        "parties": [
            {"role": "Petitioner", "name": "Nexora Infra Private Limited", "type": "Corporate Entity"},
            {"role": "Respondent", "name": "Apex Global Energy Corporation", "type": "Foreign Corporate Entity"},
            {"role": "Counsel for Petitioner", "name": "Senior Advocate Rajiv Nayar with Adv. Kunal Mehra", "type": "Advocate"},
            {"role": "Counsel for Respondent", "name": "Senior Advocate Darius Khambata with Adv. Priya Shah", "type": "Advocate"}
        ],
        "provisions": [
            {
                "act_name": "Arbitration and Conciliation Act, 1996",
                "section_or_article": "Section 9",
                "context": "Application for interim relief seeking preservation of disputed funds and bank guarantee restraint pending constitution of arbitral tribunal.",
                "supporting_quote": "A petition under Section 9 of the Act is maintainable prior to the constitution of the Arbitral Tribunal only where urgent protective measures are demonstrated to prevent irreparable loss.",
                "page_number": 1,
                "is_applied": True,
                "application_type": "Interpreted & Applied"
            },
            {
                "act_name": "Arbitration and Conciliation Act, 1996",
                "section_or_article": "Section 11",
                "context": "Contemplated appointment of sole arbitrator in international commercial arbitration.",
                "supporting_quote": "The petitioner has already initiated steps under Section 11 for the appointment of an independent arbitrator.",
                "page_number": 2,
                "is_applied": False,
                "application_type": "Cited / Mentioned"
            },
            {
                "act_name": "Code of Civil Procedure, 1908",
                "section_or_article": "Order XXXIX Rules 1 & 2",
                "context": "General equitable principles governing grant of temporary injunctions applied to arbitration petitions.",
                "supporting_quote": "While exercising jurisdiction under Section 9, the Court must be guided by the settled principles of Order XXXIX Rules 1 and 2 of the CPC.",
                "page_number": 2,
                "is_applied": True,
                "application_type": "Applied by Analogy"
            }
        ],
        "summary": {
            "case_overview": "This commercial petition under Section 9 of the Arbitration and Conciliation Act, 1996 seeks interim protection against the encashment of unconditional bank guarantees amounting to INR 42 Crores arising out of a pipeline engineering contract.",
            "background": "The petitioner was awarded a sub-contract for setting up transmission pipelines. Disputes arose concerning project delays caused by pandemic force majeure events and change-of-scope orders. The respondent issued a termination notice and threatened immediate encashment of performance bank guarantees.",
            "main_legal_issue": "Whether the petitioner has established egregious fraud or irretrievable injustice sufficient to restrain the invocation of unconditional performance bank guarantees under Section 9 of the Arbitration Act pending arbitral constitution?",
            "arguments": {
                "petitioner_arguments": "The petitioner contended that the respondent's invocation was fraudulent and premature because delays were directly caused by the respondent's failure to provide right-of-way clearances, and encashment would force the petitioner into corporate insolvency.",
                "respondent_arguments": "The respondent argued that bank guarantees represent independent contracts between the bank and beneficiary; courts cannot injunct invocation except in established fraud of egregious nature, which was not pleaded."
            },
            "court_reasoning": "The Court observed that settled commercial law strictly restricts judicial interference with unconditional bank guarantees. Demands under bank guarantees cannot be restrained on allegations of ordinary breach of contract. However, regarding the disputed retention sum of INR 14 Crores already held by respondent, an ad-interim status quo is warranted until the arbitral tribunal convenes.",
            "final_order": "This is an INTERIM ORDER and does not determine final liability. The Court declined to stay the bank guarantees, but directed the respondent to deposit the retention sum in an interest-bearing escrow account and referred the dispute to an emergency arbitrator.",
            "important_takeaways": [
                "This document is an INTERIM ORDER, not a final judgment; the substantive contract dispute remains to be resolved by the arbitral tribunal.",
                "Courts will not injunct unconditional bank guarantees under Section 9 absent demonstrated egregious fraud or exceptional irretrievable harm.",
                "Interim protection is balanced by directing preservation of liquid assets in escrow accounts pending arbitration.",
                "Parties are directed to expedite arbitral tribunal constitution under Section 11."
            ]
        },
        "evidence_items": [
            {
                "fact": "Section 9 jurisdiction requires demonstration of urgent protective measures prior to arbitral tribunal formation.",
                "quote": "A petition under Section 9 of the Act is maintainable prior to the constitution of the Arbitral Tribunal only where urgent protective measures are demonstrated to prevent irreparable loss.",
                "page": 1,
                "section_or_para": "Paragraph 4"
            },
            {
                "fact": "Courts will not interfere with unconditional bank guarantees based purely on allegations of contractual breach.",
                "quote": "Settled jurisprudence holds that unconditional bank guarantees constitute independent obligations, immune from judicial interference save in cases of established fraud or special equities.",
                "page": 2,
                "section_or_para": "Paragraph 9"
            },
            {
                "fact": "The Court ordered status quo and escrow deposit as an interim measure without resolving the full dispute.",
                "quote": "This interim direction shall remain in force until the arbitral tribunal is formally constituted and considers Section 17 applications.",
                "page": 3,
                "section_or_para": "Paragraph 15 (Operative Order)"
            }
        ],
        "pages_text": {
            1: """IN THE HIGH COURT OF DELHI AT NEW DELHI
(COMMERCIAL DIVISION)
O.M.P. (I) (COMM.) NO. 342 OF 2023

IN THE MATTER OF:
Nexora Infra Private Limited                         ...Petitioner
VERSUS
Apex Global Energy Corporation                       ...Respondent

CORAM:
HON'BLE MR. JUSTICE PRATEEK JALAN

INTERIM ORDER
PRATEEK JALAN, J.

1. The present petition has been preferred under Section 9 of the Arbitration and Conciliation Act, 1996 [hereinafter 'the Act'], seeking urgent ad-interim interim protection to restrain the respondent from invoking Performance Bank Guarantees totaling INR 42,00,00,000/-.

4. A petition under Section 9 of the Act is maintainable prior to the constitution of the Arbitral Tribunal only where urgent protective measures are demonstrated to prevent irreparable loss. The petitioner claims that invocation of bank guarantees during active reconciliation negotiations violates commercial good faith.""",
            2: """O.M.P. (I) (COMM.) NO. 342 OF 2023                              [PAGE 2]

7. Mr. Rajiv Nayar, learned Senior Counsel appearing for the petitioner, submitted that the delay in executing the work was caused entirely by the respondent's delay in providing Right of User (RoU) permissions. It is submitted that the petitioner has already initiated steps under Section 11 for the appointment of an independent arbitrator.

9. While exercising jurisdiction under Section 9, the Court must be guided by the settled principles of Order XXXIX Rules 1 and 2 of the CPC. Settled jurisprudence holds that unconditional bank guarantees constitute independent obligations, immune from judicial interference save in cases of established fraud or special equities. The threshold of egregious fraud vitiating the underlying transaction has not been satisfied on the present record.""",
            3: """O.M.P. (I) (COMM.) NO. 342 OF 2023                              [PAGE 3]

12. However, with respect to the retention fund of INR 14 Crores withheld by the respondent, the balance of convenience dictates preservation of the asset so that the arbitral award is not rendered unenforceable.

15. Consequently, the prayer to restrain invocation of the bank guarantees is declined. However, the respondent is directed to maintain the retention amount of INR 14 Crores in an interest-bearing escrow account. This interim direction shall remain in force until the arbitral tribunal is formally constituted and considers Section 17 applications.

16. It is clarified that this order is purely an interim procedural protection and expresses no final opinion on the merits of contractual claims.

PRATEEK JALAN, J.
NOVEMBER 14, 2023
NEW DELHI"""
        }
    },

    "constitutional_privacy": {
        "id": "constitutional_privacy",
        "title": "Constitutional Law: Article 21 Fundamental Right to Privacy",
        "case_name": "Justice K.S. Puttaswamy (Retd.) & Anr. v. Union of India & Ors.",
        "court_name": "Supreme Court of India",
        "case_number": "Writ Petition (Civil) No. 494 of 2012",
        "decision_date": "24 August 2017",
        "bench": "Hon'ble Nine-Judge Constitution Bench (per J.S. Khehar, CJI, J. Chelameswar, S.A. Bobde, R.K. Agrawal, R.F. Nariman, A.M. Sapre, D.Y. Chandrachud, S.K. Kaul, S. Abdul Nazeer, JJ.)",
        "case_category": "Constitutional",
        "document_type": "Judgment",
        "total_pages": 4,
        "parties": [
            {"role": "Lead Petitioner", "name": "Justice K.S. Puttaswamy (Retd.)", "type": "Individual / Former Judge"},
            {"role": "Respondent 1", "name": "Union of India (Ministry of Law & Justice)", "type": "Union Government"},
            {"role": "Respondent 2", "name": "Unique Identification Authority of India (UIDAI)", "type": "Statutory Authority"},
            {"role": "Interveners", "name": "Centre for Internet & Society, Digital Freedom Collective", "type": "Non-Governmental Organization"}
        ],
        "provisions": [
            {
                "act_name": "Constitution of India",
                "section_or_article": "Article 21",
                "context": "Protection of life and personal liberty, held to intrinsically incorporate privacy as a fundamental human right.",
                "supporting_quote": "The right to privacy is protected as an intrinsic part of the right to life and personal liberty under Article 21 and as a part of the freedoms guaranteed by Part III of the Constitution.",
                "page_number": 1,
                "is_applied": True,
                "application_type": "Interpreted & Applied (Constitutional Benchmark)"
            },
            {
                "act_name": "Constitution of India",
                "section_or_article": "Article 14",
                "context": "Equality before the law and protection against arbitrary state action in data collection.",
                "supporting_quote": "Any state intrusion into individual privacy must satisfy the threefold requirement of legality, legitimate state aim, and proportionality under Articles 14, 19, and 21.",
                "page_number": 3,
                "is_applied": True,
                "application_type": "Applied / Test of Proportionality"
            },
            {
                "act_name": "Constitution of India",
                "section_or_article": "Article 32",
                "context": "Remedies for enforcement of fundamental rights via writ petition directly before the Supreme Court.",
                "supporting_quote": "This petition was instituted under Article 32 of the Constitution challenging the mandatory collection of biometric data.",
                "page_number": 1,
                "is_applied": False,
                "application_type": "Procedural Inception"
            }
        ],
        "summary": {
            "case_overview": "A historic landmark nine-judge Constitution Bench judgment unanimously holding that the Right to Privacy is a fundamental right protected under Part III of the Constitution of India, primarily emanating from Article 21.",
            "background": "Writ petitions challenged the constitutional validity of the Aadhaar biometric identity scheme. The Union Government argued that privacy is not a fundamental right under the Indian Constitution, relying on older eight-judge bench decisions in M.P. Sharma (1954) and Kharak Singh (1962). The matter was referred to a nine-judge bench to definitively settle the constitutional question.",
            "main_legal_issue": "Whether the Constitution of India guarantees a fundamental right to privacy, and whether the earlier decisions in M.P. Sharma and Kharak Singh declaring that privacy is not a fundamental right remain good law?",
            "arguments": {
                "petitioner_arguments": "Petitioners argued that privacy is an essential attribute of human dignity, personal autonomy, and liberty guaranteed by Article 21, and that technological advances make information privacy imperative.",
                "respondent_arguments": "The Union of India contended that the framers of the Constitution consciously excluded privacy from Part III, and privacy is merely a common law right subject to ordinary statutory regulation."
            },
            "court_reasoning": "The nine judges unanimously overruled M.P. Sharma and Kharak Singh to the extent they held privacy was not a fundamental right. The Court reasoned that privacy is inalienable to human dignity and freedom. However, privacy is not absolute; state intrusion must satisfy the triple test: (1) Legality (statutory backing), (2) Legitimate state goal, and (3) Proportionality.",
            "final_order": "The reference was answered unanimously declaring that Privacy is a fundamental right under Article 21. The specific challenge to the Aadhaar statutory provisions was directed to be placed before a regular five-judge bench for adjudication based on the declared principles.",
            "important_takeaways": [
                "Right to Privacy is declared a fundamental right under Article 21 and Part III of the Constitution of India.",
                "M.P. Sharma (1954) and Kharak Singh (1962) overruled to the extent they denied privacy as a constitutional right.",
                "Privacy is not absolute; state actions must pass the three-prong test of Legality, Legitimate State Aim, and Proportionality.",
                "Informational privacy and bodily autonomy are intrinsic components of individual liberty in the digital age."
            ]
        },
        "evidence_items": [
            {
                "fact": "Right to Privacy is explicitly declared as an intrinsic component of Article 21.",
                "quote": "The right to privacy is protected as an intrinsic part of the right to life and personal liberty under Article 21 and as a part of the freedoms guaranteed by Part III of the Constitution.",
                "page": 1,
                "section_or_para": "Paragraph 3 (Unanimous Order of Court)"
            },
            {
                "fact": "Earlier precedents in M.P. Sharma and Kharak Singh were expressly overruled.",
                "quote": "The decision in M.P. Sharma, to the extent that it holds that the right to privacy is not protected by the Constitution, stands overruled.",
                "page": 2,
                "section_or_para": "Paragraph 7"
            },
            {
                "fact": "Any state intrusion into privacy must satisfy legality, legitimate purpose, and proportionality.",
                "quote": "Any state intrusion into individual privacy must satisfy the threefold requirement of legality, legitimate state aim, and proportionality under Articles 14, 19, and 21.",
                "page": 3,
                "section_or_para": "Paragraph 14"
            }
        ],
        "pages_text": {
            1: """IN THE SUPREME COURT OF INDIA
CIVIL ORIGINAL JURISDICTION
WRIT PETITION (CIVIL) NO. 494 OF 2012

Justice K.S. Puttaswamy (Retd.) & Anr.              ...Petitioners
VERSUS
Union of India & Ors.                              ...Respondents

CORAM:
HON'BLE THE CHIEF JUSTICE J.S. KHEHAR
HON'BLE MR. JUSTICE J. CHELAMESWAR
HON'BLE MR. JUSTICE S.A. BOBDE
HON'BLE MR. JUSTICE R.K. AGRAWAL
HON'BLE MR. JUSTICE R.F. NARIMAN
HON'BLE MR. JUSTICE A.M. SAPRE
HON'BLE DR. JUSTICE D.Y. CHANDRACHUD
HON'BLE MR. JUSTICE S.K. KAUL
HON'BLE MR. JUSTICE S. ABDUL NAZEER

ORDER OF THE COURT
1. This petition was instituted under Article 32 of the Constitution challenging the mandatory collection of biometric data under the Aadhaar scheme. 

3. The right to privacy is protected as an intrinsic part of the right to life and personal liberty under Article 21 and as a part of the freedoms guaranteed by Part III of the Constitution. Privacy recognizes the autonomy of the individual and postulates that there is an inviolable space reserved for the individual.""",
            2: """WRIT PETITION (CIVIL) NO. 494 OF 2012                          [PAGE 2]

5. The reference arose because the Union of India submitted that earlier decisions of larger benches, notably an eight-judge bench in M.P. Sharma v. Satish Chandra (1954) and a six-judge bench in Kharak Singh v. State of U.P. (1962), had held that the Indian Constitution does not confer a fundamental right to privacy.

7. The decision in M.P. Sharma, to the extent that it holds that the right to privacy is not protected by the Constitution, stands overruled. Kharak Singh, to the extent that it observed that the right to privacy is not a guaranteed right, also stands overruled.

9. Privacy is not created by the Constitution; it is an inalienable natural right which the Constitution recognizes as fundamental to human dignity.""",
            3: """WRIT PETITION (CIVIL) NO. 494 OF 2012                          [PAGE 3]

12. Like other fundamental rights, the right to privacy is not an absolute right. An invasion of privacy by the State must be justified on the basis of a law which stipulates a procedure which is just, fair and reasonable.

14. Any state intrusion into individual privacy must satisfy the threefold requirement of legality, legitimate state aim, and proportionality under Articles 14, 19, and 21. There must be a law in existence, the law must pursue a legitimate goal, and the means adopted must be proportional to the object sought to be achieved.

16. Informational privacy forms an essential facet of personal privacy in an era dominated by electronic databases and artificial intelligence.""",
            4: """WRIT PETITION (CIVIL) NO. 494 OF 2012                          [PAGE 4]

20. We answer the reference in the following terms:
(i) The right to privacy is a fundamental right. It is a harmonious component of Part III of the Constitution.
(ii) The decisions in M.P. Sharma and Kharak Singh stand overruled to the extent noted.
(iii) The writ petitions challenging the statutory Aadhaar scheme shall now be placed before the regular bench for disposal on merits.

Ordered accordingly.

................................................CJI.
(J.S. KHEHAR)
................................................J.
(J. CHELAMESWAR)
................................................J.
(D.Y. CHANDRACHUD)
NEW DELHI;
AUGUST 24, 2017."""
        }
    }
}
