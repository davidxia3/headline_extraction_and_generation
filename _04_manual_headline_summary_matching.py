import pandas as pd


df = pd.read_csv("agenda_segments/20250401_REG.csv")
df.loc[23, "true_headline"] = """Open-Ended Professional Services Contracts Add 27 Unspecified New Vendors"""
df.loc[23, "true_summary"] = """- Open-ended professional services contracts allow vendors to provide on-call professional services for work orders estimated to cost $100,000 or less.\n- The program’s goal is to enable City departments to contract services on a rolling basis without seeking Council approval for each request.\n- Services include architecture, interior design, and historic consulting, among others.\n- New vendors will be added to the program on a rolling basis, but any new additions will require Council approval.\n- Councilperson Charland expressed concern that the “fairly self-governing” system of distributing work could lead departments to overlook minority contractors."""
df.loc[27, "true_headline"] = """Portable Restroom Back Payment Sparks Inquiries into the Prevalence of Closed Public Restrooms in City Parks"""
df.loc[27, "true_summary"] = """- A bill covering $35k in expenses for portable bathrooms led to a discussion about the number of broken permanent public restrooms in the city’s parks.\n- Director Hornstein of the Department of Public Works did not have an exact count of closed public restrooms to share with Council.\n- There are 20 open public restrooms in city parks.\n- To restore inoperable restrooms, Director Hornstein stated that public approval and tax funding would be needed for:\n  - An assessment of which restrooms are closed and what repairs and maintenance are required.\n  - The actual repairs and maintenance, which will likely be significant given how long some have been closed.\n  - A program to maintain the restrooms once they are reopened.\n- The city spent $219,000 on portable restrooms in parks that lack functioning permanent public restrooms.\n- Council members agreed that there should be a plan to begin addressing this long-standing issue."""

df.to_csv("agenda_segments/20250401_REG.csv", index=False)


df = pd.read_csv("agenda_segments/20250402_STA.csv")
df.loc[12, "true_headline"] = """Council to Approve Funding for Recruitment Video Aimed at Addressing Police Shortages"""
df.loc[12, "true_summary"] = """- The Police Department is requesting approval to spend $32K from a State grant on a new recruitment video to be developed by Kicker, Inc.\n- Videos are expected to include “exciting and proud images of Pittsburgh Police Officers at work in various positions, including Patrol, K-9 Unit, Investigators, SWAT, Motorcycle Unit, Mounted Patrol, River Patrol, Special Victims Unit, Narcotics/Vice, and Computer Crimes Unit” as well as iconic Pittsburgh imagery.\n- Council noted the need for new recruitment efforts and was pleased to hear that the number of people taking the civil service exam has begun to increase. They hope the videos are as successful as they have been in other cities.\n- The videos will primarily be used across social media platforms and YouTube."""
df.loc[17, "true_headline"] = """14 Acre Bakery Square Expansion Moves Forward with Two Key Amendments Ready for Public Hearing"""
df.loc[17, "true_summary"] = """- The expansion will encompass 14 acres west along Penn Avenue in the Larimer and East Liberty neighborhoods.\n- The standout initiative is the Build 100 program, which calls for Walnut Capital to contribute $6 million and commit to raising another $19 million toward creating 100 affordable homes for purchase.\n- This work is the product of a Community Benefits Agreement between the Larimer Consensus Group, the Village Collaborative, and Walnut Capital.\n- Council sent the proposed amendments to the Planning Commission on July 6 and July 12, 2023, and received the Commission’s report and recommendation for both on January 24, 2025.\n- The 4/2 vote allows for two bills—one delineating new block and lot numbers and the other detailing building code and other requirements within the subdistrict—to proceed to a public hearing."""

df.to_csv("agenda_segments/20250402_STA.csv", index=False)


df = pd.read_csv("agenda_segments/20250408_POS.csv")
df.loc[0, "true_headline"] = """Mayor's Vision Zero Plan Appears on Track, Still Awaiting Traffic Fatality Data"""
df.loc[0, "true_summary"] = """- In Pittsburgh, an average of 20 people die in traffic crashes each year.\n- Block-by-block data reveals that 83% of serious injury crashes and 76% of fatal crashes occur on just 10% of the City’s roadways.\n- Pittsburgh joined Vision Zero—a worldwide movement to end all traffic fatalities and serious injuries—in March 2024.\n  - During the initiative's first year, areas with traffic calming measures saw average vehicle speeds decrease by 7 mph and a 55% drop in speeding instances. Areas with replaced traffic signals experienced 33% fewer crashes.\n- 2024 crash data (fatal, serious injury, pedestrian, and bicycle) will not be available until this summer.\n- Of the 57 tasks stated in the report, 30 are marked as completed or completed and ongoing.\n  - These tasks range from passing Automated Red Light Enforcement legislation and securing large project funding to relocating or adding individual street signs.\n  - An additional 18 tasks are on track to be completed in 2025."""

df.to_csv("agenda_segments/20250408_POS.csv", index=False)


df = pd.read_csv("agenda_segments/20250408_REG.csv")
df.loc[8, "true_headline"] = """Council Seeks State Assistance in Eliminating the City’s Litter and Illegal Dumpsites"""
df.loc[8, "true_summary"] = """- Councilperson Charland raised the Issue, stating, “Being as filthy as we are is a choice, and we need to stop making that choice.”\n- While supportive, Councilpersons Gross, Mosley, and Council President Lavelle expressed concern that classifying the initial request could detract from addressing larger issues, such as the transit funding crisis.\n- Requested resources could include borrowing equipment, contracts, and funding.\n- Council members acknowledged that Public Works is doing its best but is stretched thin.\n- Local cleanups often occur through various neighborhood and community organizations.\n- A new City program, in partnership with the Center for Employment Opportunities, will hire people leaving incarceration to pick up trash; it begins this weekend in Homewood."""
df.loc[10, "true_headline"] = """Untested Sexual Assault Kits to Be Processed"""
df.loc[10, "true_summary"] = """- The Department of Public Safety requested $37,000 from a previously awarded 2023 National Sexual Assault Kit Initiative Grant.\n- Funds will primarily support overtime for City detectives investigating backlogged sexual assault cases.\n- The Bureau has already identified untested kits using previous grant funds.\n  - The number of untested kits, or whether the funds would be sufficient to test them, was not mentioned. Informup reached out to the Department for specifics, but we have not received a response by the time of publication.\n- Additional work will include pulling kits, writing reports, transporting kits to the Crime Lab, and any follow‑up investigations.\n- $1,000 will be allocated to create a soft interview room for the Pittsburgh Bureau of Police.\n  - Current rooms are designed for interviewing suspects and are not conducive to victims sharing difficult personal experiences.\n- The request received a unanimous affirmative recommendation."""
df.loc[32, "true_headline"] = """Council to Approve Funding for Recruitment Video Aimed at Addressing Police Shortages"""
df.loc[32, "true_summary"] = """- The Police Department is requesting approval to spend $32K from a State grant on a new recruitment video to be developed by Kicker, Inc.\n- Videos are expected to include “exciting and proud images of Pittsburgh Police Officers at work in various positions, including Patrol, K-9 Unit, Investigators, SWAT, Motorcycle Unit, Mounted Patrol, River Patrol, Special Victims Unit, Narcotics/Vice, and Computer Crimes Unit” as well as iconic Pittsburgh imagery.\n- Council noted the need for new recruitment efforts and was pleased to hear that the number of people taking the civil service exam has begun to increase. They hope the videos are as successful as they have been in other cities.\n- The videos will primarily be used across social media platforms and YouTube."""

df.to_csv("agenda_segments/20250408_REG.csv", index=False)


df = pd.read_csv("agenda_segments/20250409_STA.csv")
df.loc[13, "true_headline"] = """City Receives State Funds for New Lighting Along Penn Ave in East Liberty"""
df.loc[13, "true_summary"] = """- The City has been awarded funds from the State to install 96 new LED lights along Penn Avenue, from the Target at Spirit St. to Negley Ave.\n- This lighting upgrade will complement the LED Streetlight Modernization Project, which aims to replace high-pressure sodium fixtures across the City with LED fixtures.\n  - LED lights use less electricity and produce less light pollution than high-pressure sodium lights."""

df.to_csv("agenda_segments/20250409_STA.csv", index=False)


df = pd.read_csv("agenda_segments/20250415_REG.csv")
df.loc[8, "true_headline"] = """$40,000 Contract with Law Firm for “Immigration Matters” Authorized"""
df.loc[8, "true_summary"] = """- Council authorized a $40,000 contract with Fragomen, Del Rey, Bernsen & Loewy, LLP, a global immigration law firm.\n- The authorization was discussed in an executive session closed to the public and was not presented in Standing Committee before approval."""
df.loc[22, "true_headline"] = """City Receives State Funds for New Lighting Along Penn Ave in East Liberty"""
df.loc[22, "true_summary"] = """- The City has been awarded funds from the State to install 96 new LED lights along Penn Avenue, from the Target at Spirit St. to Negley Ave.\n- This lighting upgrade will complement the LED Streetlight Modernization Project, which aims to replace high-pressure sodium fixtures across the City with LED fixtures.\n  - LED lights use less electricity and produce less light pollution than high-pressure sodium lights."""

df.to_csv("agenda_segments/20250415_REG.csv", index=False)


df = pd.read_csv("agenda_segments/20250416_STA.csv")
df.loc[2, "true_headline"] = """Council Reopens Discussion of the Process to Purchase City Property After a Rescinded Sale"""
df.loc[2, "true_summary"] = """- A resident who purchased a $40,000 house through the City’s Real Estate Division in 2022 requested to rescind the sale and receive a refund of the required 10% earnest money.\n- The purchaser claims the house deteriorated during the sale process.\n  - The sale process—which includes a quiet title lawsuit—typically takes 12–18 months but can extend to 24 months.\n- Properties sold by the City are primarily vacant lots acquired through sheriff’s sales.\n- Buyers must be approved by the City, and sales must be approved by Council.\n- Councilmember Coghill expressed concern about the length of the process and the lack of property stabilization.\n- The refund was approved with no next steps proposed."""
df.loc[9, "true_headline"] = """Untested Sexual Assault Kits to Be Processed"""
df.loc[9, "true_summary"] = """- The Department of Public Safety requested $37,000 from a previously awarded 2023 National Sexual Assault Kit Initiative Grant.\n- Funds will primarily support overtime for City detectives investigating backlogged sexual assault cases.\n- The Bureau has already identified untested kits using previous grant funds.\n  - The number of untested kits, or whether the funds would be sufficient to test them, was not mentioned. Informup reached out to the Department for specifics, but we have not received a response by the time of publication.\n- Additional work will include pulling kits, writing reports, transporting kits to the Crime Lab, and any follow‑up investigations.\n- $1,000 will be allocated to create a soft interview room for the Pittsburgh Bureau of Police.\n  - Current rooms are designed for interviewing suspects and are not conducive to victims sharing difficult personal experiences.\n- The request received a unanimous affirmative recommendation."""
df.loc[14, "true_headline"] = """Proposed July 2024 Contract for Shelter Services Held Another Five Weeks"""
df.loc[14, "true_summary"] = """- The $1,500,000 contract with Auberle—a long‑established local social services provider—has been held in committee since July 2024.\n- The contract will be fully funded by the Department of Housing and Urban Development’s HOME Investment Partnerships American Rescue Plan (HOME‑ARP) program, designed to reduce homelessness and increase housing stability.\n- Funds may be used for private units, temporary shelter, and costs associated with acquisition, new construction, or rehabilitation of existing structures.\n- Councilmember Wilson updated Council that a HUD representative has reviewed an updated proposal giving preference to homeless families. A meeting with Urban Design Ventures is scheduled for April 17 to plan the amendment process, which will include a yet to be scheduled public hearing."""

df.to_csv("agenda_segments/20250416_STA.csv", index=False)


df = pd.read_csv("agenda_segments/20250422_POS.csv")

df.to_csv("agenda_segments/20250422_POS.csv", index=False)


df = pd.read_csv("agenda_segments/20250422_REG.csv")
df.loc[18, "true_headline"] = """Riverlife Barge Venue to Dock at Allegheny Landing Park"""
df.loc[18, "true_summary"] = """- Council recommended Riverlife’s request to dock a sectional spud barge at Allegheny Landing Park (North Shore, just East of PNC Park).\n  - A spud barge is a semi-permanent floating platform that can be assembled from multple sctions joined together\n- The barge will be open to the public via the City-owned dock and will:\n  - “celebrate Pittsburgh’s rivers through primarily free, accessible, and sustainable activities and events.”\n- Riverlife is selecting a vendor for a concession stand.\n- The barge is expected to open in June."""
df.loc[19, "true_headline"] = """Bill to Allow Pollinator Gardens and Natural Landscapes Introduced"""
df.loc[19, "true_summary"] = """- Bill would exempt intentional plantings of native Pennsylvania vegetation from code violations to enhance biodiversity and protect the City’s environment.\n- The exemption covers:\n  - Native Gardens: A planned garden using plants that naturally grow in Pennsylvania and are suited to its climate and soil.\n  - Pollinator Gardens: A garden designed to attract and support pollinators like bees, butterflies, and hummingbirds by offering food, water, and shelter.\n  - Rain Gardens: A shallow, landscaped area with native plants that captures and filters rainwater runoff.\n- Current City Code prohibits these landscapes and all plant and weed growth over 10 inches on residential properties.\n- Residents must register their gardens with the City before planting.\n- Violations incur a $15-per-day fine.\n- Bill will be discussed at next week’s Standing Committee meeting."""
df.loc[21, "true_headline"] = """Challenged Historic Designation for Former Gay Bar to Receive Public Hearing"""
df.loc[21, "true_summary"] = """- Donny’s Place operated from 1972 to 2022 and served as an outreach center during the AIDS crisis.\n- If approved, the Polish Hill site would become Pittsburgh’s first LGBTQ+ historic landmark.\n- The estate of the late owner, Donald Thinnes, opposes the nomination; Thinnes entered a 2019 sales agreement to develop the property into townhouses.\n- The Planning Commission voted against the nomination, citing lack of owner support, fire damage, and testimony that the bar was not unique.\n- The historic designation is sought by two Polish Hill residents and Preservation Pittsburgh.\n- The date for the public hearing has yet to be scheduled."""
df.loc[38, "true_headline"] = """Untested Sexual Assault Kits to Be Processed"""
df.loc[38, "true_summary"] = """- The Department of Public Safety requested $37,000 from a previously awarded 2023 National Sexual Assault Kit Initiative Grant.\n- Funds will primarily support overtime for City detectives investigating backlogged sexual assault cases.\n- The Bureau has already identified untested kits using previous grant funds.\n  - The number of untested kits, or whether the funds would be sufficient to test them, was not mentioned. Informup reached out to the Department for specifics, but we have not received a response by the time of publication.\n- Additional work will include pulling kits, writing reports, transporting kits to the Crime Lab, and any follow‑up investigations.\n- $1,000 will be allocated to create a soft interview room for the Pittsburgh Bureau of Police.\n  - Current rooms are designed for interviewing suspects and are not conducive to victims sharing difficult personal experiences.\n- The request received a unanimous affirmative recommendation."""

df.to_csv("agenda_segments/20250422_REG.csv", index=False)


df = pd.read_csv("agenda_segments/20250423_PUB.csv")
df.loc[1, "true_headline"] = """'Tiny Lots' Approved After Spirited Debate"""
df.loc[1, "true_summary"] = """- The amendment to the residential zoning ordinance reduces minimum lot sizes for all density levels and removes the minimum unit-size requirement for apartments and condos.\n  - All other zoning rules remain unchanged.\n- While Council generally supported the text, some members raised concerns about:\n  - Timing the vote right after this week’s severe storm\n  - Whether zoning changes should be made individually or all at once\n  - If minimum lot sizes were the most critical amendment among many under consideration\n- The bill received an affirmative recommendation, passing 5–1 with two abstentions. Councilperson Gross voted against with Councilpersons Lavelle and Warwick abstaining. Councilperson Mosley was absent.\n- Current Min Lot Size:\n  - Very Low Density (VL): 8,000 sq ft\n  - Low Density (L): 5,000 sq ft\n  - Moderate Density (M): 3,200 sq ft\n  - High Density (H): 1,800 sq ft\n  - Very High Density (VH): 1,200 sq ft\n- Proposed Min Lot Size:\n  - Very Low Density (VL): 6,000 sq ft\n  - Low Density (L): 3,000 sq ft\n  - Moderate Density (M): 2,400 sq ft\n  - High Density (H): 1,200 sq ft\n  - Very High Density (VH): None"""

df.to_csv("agenda_segments/20250423_PUB.csv", index=False)


df = pd.read_csv("agenda_segments/20250423_STA.csv")
df.loc[5, "true_headline"] = """$40,000 Contract with Law Firm for “Immigration Matters” Authorized"""
df.loc[5, "true_summary"] = """- Council authorized a $40,000 contract with Fragomen, Del Rey, Bernsen & Loewy, LLP, a global immigration law firm.\n- The authorization was discussed in an executive session closed to the public and was not presented in Standing Committee before approval.\n- InformUp contacted both the Councilperson Lavelle's office and the law firm for additional information but received no response by publication time."""

df.to_csv("agenda_segments/20250423_STA.csv", index=False)

