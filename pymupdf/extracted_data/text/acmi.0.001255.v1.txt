Preprint DOI: https://doi.org/10.1099/acmi.0.001255.v1 

Posted on July 16, 2026 

© 2026 The Authors. This is an open-access article distributed under the terms of the Creative Commons Attribution License. 

- 1 **Design, implementation, and reflections on delivering** 

- 2 **machine learning workshops for medical microbiology and** 

- 3 **infection science** 

- 4 **1.1 Author names** 

- 5 _Benjamin R. McFadden* (1)_ 

- 6 _Mark Reynolds (1)_ 

- 7 _Timothy J.J. Inglis (2,3)_ 

- 8 **1.2 Affiliation(s)** 



- 9 _1)_ University of Western Australia, School of Physics, Mathematics and 

- 10 Computing, Perth, 6009, Australia 

- 11 _2)_ University of Western Australia, Schools of Medicine and Biomedical Science, 12 Perth, 6009, Australia 

- 13 _3)_ Department of Microbiology, PathWest Laboratory Medicine WA, QEII Medical 14 Centre, Nedlands, 6009, Australia. 15 

- 16 **1.3 Corresponding author and email address** 

- 17 _Benjamin R. McFadden_ 



- 18 _benjamin.mcfadden@research.uwa.edu.au_ 

19 

- 20 **1.4 Keywords** 

- 21 _Machine learning, workshop, medical microbiology, infection science, artificial intelligence_ 

22 

- 23 **2.  Abstract** 

- 24 Increasingly, machine learning (ML) and artificial intelligence (AI) methods are being applied 

- 25 in medical microbiology and infection science. With this comes the challenge of educating 

- 26 professionals in these domains on the fundamental theory and methods of ML and AI in a 

- 27 way that is time-efficient and grounded in practical application. This article outlines the 

- 28 design, implementation, and reflections on delivering _“Using Data Science and Machine_ 

- 29 _Learning for Infection Science: A Hands-On Introduction”,_ a recurring one-day workshop 

- 30 created to introduce data science and ML concepts to infection science and medical 

- 31 microbiology students and professionals. The workshop provides participants with the 

- 32 opportunity for experiential learning using _Orange,_ a no-code, open-source, and free-to-use 

- 33 data mining software application, where participants are exposed to the fundamentals of 



- 34 the ML lifecycle. By the conclusion of the one-day workshop, participants gain experience 

- 35 developing end-to-end analytical pipelines for tabular datasets, with a specific example 

- 36 focused on blood culture outcome prediction. The workshop emphasises transparency, 

- 37 reproducibility, and open science, promoting critical awareness of how data science can be 

- 38 applied within participants’ own domain specialty. This article details the curriculum design, 

- 39 practical implementation, and delivery of the workshop. Additionally, we reflect on the 

- 40 lessons learned and directions for future iterations of the workshop. 

- 41 

# 42 **3.  Impact statement** 

- 43 Artificial intelligence (AI) and machine learning (ML) are increasingly used in medical 

- 44 microbiology and infection science, but many professionals have limited time or opportunity 

- 45 to learn these methods in a practical, accessible way. This article describes the development 

- 46 and delivery of a one-day workshop designed to introduce students and professionals to the 

- 47 key ideas behind data science and machine learning. The workshop uses Orange, a free, 

- 48 open-source, no-code software tool, so participants can focus on understanding the 

- 49 machine learning process without needing advanced programming skills. 

- 50 Through hands-on activities, participants learn how to build simple analytical workflows 

- 51 using real-world style tabular data. The workshop also highlights important principles such 

- 52 as transparency, reproducibility, and open science, helping participants think critically about 53 how these methods could be used responsibly in their own work. 

- 54 By sharing the workshop design, teaching approach, and lessons learned, this article 

- 55 provides a practical model for building machine learning education within medical 

- 56 microbiology and infection science. It supports the development of a more confident and 57 informed workforce able to engage with emerging AI, ML, and data science tools. 

58 

- 59 **4.  Data summary** 

- 60 The authors confirm that no data was generated or reused in the process of producing this 61 paper. 

- 62 

- 63 **5.  Introduction** 



- 64 Digital transformation across healthcare has led to an unprecedented accumulation of 

- 65 laboratory, clinical, and infection-related data. In the context of clinical microbiology and 

- 66 infection science, this data holds the potential to support a variety of areas, including 

- 67 diagnostic decision-making, antimicrobial resistance monitoring, and process improvement. 

- 68 Alongside the increasing volume of data, machine learning (ML) and artificial intelligence 69 (AI) methods are being applied more widely to detect patterns in datasets and develop 

- 70 predictive models [1]. However, many infection science professionals lack formal training in 

- 71 computational methods, which limits the translation of raw data into actionable insights and 72 applications. Furthermore, as research on the application of these methods increases, there 

- 73 is a need for infection science and clinical microbiology professionals to have the knowledge 

- 74 to support peer-review and aid in translating applications into practice. In the literature, 

- 75 there are previously published tutorials and workshops for healthcare professionals and for 

- 76 those without ML domain expertise [2, 3]. However, to the best of our knowledge, there are 

- 77 no published papers discussing in-person data science and ML workshops tailored to 78 infection science. 

- 79 To address this gap in training amongst those working and/or studying in the clinical 

- 80 microbiology and infection science domain, authors Benjamin McFadden (BM) and Timothy 81 Inglis (TI) designed the _“Using Data Science and Machine Learning for Infection Science: A_ 82 _Hands-On Introduction”_ one-day workshops. Since 2024, the workshop has been delivered 

- 83 at the ECCMID conference in April 2024 (Barcelona,Spain), and the ESCMID global 

- 84 conference in April 2025 (Vienna, Austria) and April 2026 (Munich, Germany) with BM and TI 

- 85 both present to deliver these workshops. The workshop content was also delivered by BM at 

- 86 the University of Zurich Medical Microbiology Institute in June 2025, and again in April 2026. 

- 87 Prior to 2024, an earlier version of the workshop was created by TI and delivered in 2019 at 

- 88 the ECCMID conference (Amsterdam, Netherlands). The planned sequel at ECCMID 2020 was 

- 89 postponed due to the COVID-19 pandemic. Over its lifetime, the workshop has attracted 90 participants from diverse worldwide settings including hospitals, research institutes, and 91 postgraduate programs. The aim of these workshops is to teach the principles and practice 92 of reproducible ML projects from an end-to-end perspective. This means taking a holistic 93 view, starting with data preparation, and progressively working through data processing and 94 cleaning, ML modelling, and ML model evaluation. The teaching of these concepts is 

- 95 achieved using the _Orange_ data mining software [4], an open-source, no-code tool that 96 supports a range of analytical tasks, including data cleaning and transformation, 

- 97 visualisation, descriptive statistics, modelling, and model evaluation. The software also offers 98 a range of add-ons that provide additional functionality for advanced ML tasks, such as 

- 99 computer vision and natural language processing. A significant benefit of using _Orange_ is 

- 100 that it is free to download and use across multiple operating systems. As _Orange_ is a desktop 

- 101 application, it can also be used offline without an internet connection. We selected _Orange_ 

- 102 as the tool for the workshop for these reasons, so that participants were not limited by the 103 cost of software or requiring a particular operating system. 

- 104 This paper highlights and reflects on the workshop’s design, implementation and delivery, 

- 105 outlining the successes, challenges, and future directions. This paper contributes to the 

- 106 literature by providing a blueprint for teaching domain-specific computational literacy in a 

- 107 way that is time-efficient, transparent, and accessible for participants. This workshop also 

- 108 laid the foundation for the practical _Orange_ -based sessions delivered by BM at the recent 

- 109 ESCMID 4-day artificial intelligence workshop [5]. 

- 110 

- 111 **6. Rationale and motivation** 

- 112 **6.1 The skills gap in infection science** 



- 113 Infection science professionals routinely generate and interact with large volumes of digital 

- 114 data, such as culture and antimicrobial susceptibility testing results, clinical patient 

- 115 information, test turnaround times, and operational workflow metrics. Despite this, 

- 116 structured training in data analytics is often limited. Traditional laboratory education 

- 117 emphasises diagnostic reasoning and quality assurance but does not necessarily address 

- 118 statistical computing, ML, and AI. Whilst the potential of analytics may be recognised, the 

- 119 inability to translate the analytical requirements into practice limits progress. These one-day 

- 120 workshops have been designed to address this educational gap by introducing the ML 

- 121 lifecycle using an open-source tool that requires no prior programming or advanced 

- 122 computational experience. 

- 123 **6.2 Motivation** 

- 124 The workshop is designed in response to three pedagogical needs identified through 

- 125 previous experience by authors BM and TI. These include the following: 

- 126 Accessibility: Provide an entry point to data science and ML for participants without prior 

- 127 computational experience. 

- 128 Relevance: Contextualise examples around infection-science scenarios to make abstract 

- 129 concepts meaningful. This includes focusing on tabular datasets, as this is the data modality 

- 130 participants are most likely to use on a regular basis. 

- 131 Transparency: Promote transparent, open, and reproducible data science practices, 

- 132 encouraging participants to document analytical steps and adopt open-source tools where 133 possible. 

- 134 These principles align with a broader emerging philosophy regarding the importance of 135 responsible and trustworthy data science and ML implementation [6,7,8, 9]. By focusing on 

- 136 open workflow design, participants learn how to make their analyses interpretable, 

- 137 shareable, and auditable. These aspects of the analytical workflow are of fundamental 138 importance to clinical, laboratory, and research settings since they form the foundation for 139 the one-day workshops. 

- 140 **7. Workshop design and framework** 

- 141 **7.1 Design principles** 

- 142 The workshop is designed to ensure that the intended learning outcomes and teaching 143 activities are explicitly aligned [10]. Noting that assessment or evaluation tasks for the 

- 144 participants are not included. Learning outcomes are clearly articulated at the outset of the 145 workshop, and participants are informed of the knowledge and competencies they are 

- 146 expected to develop by the end of the session. Teaching activities are deliberately structured 

- 147 to support these outcomes, with an emphasis on conceptual understanding of the ML 148 lifecycle rather than narrow technical mastery. 

- 149 In addition to constructive alignment, the workshop draws on principles from experiential 

- 150 learning theory and cognitive apprenticeship. Experiential learning theory emphasises 

- 151 learning through a cycle of concrete experience, reflective observation, abstract 

- 152 conceptualisation, and active experimentation [11]. This is operationalised through live 

- 153 demonstrations of analytical workflows, hands-on sessions, and opportunities for reflection 

- 154 on methodological decisions. Cognitive apprenticeship further informed the workshop 

- 155 design by recognising that analytical proficiency develops through observation of expert 

- 156 practice, guided participation, and gradual transfer of knowledge and skills to the 

- 157 participants [12]. Guided by this educational framework and the needs of a multidisciplinary 

- 158 audience, the workshop was designed around the following principles: 

- 159 Authenticity: The analytical techniques and workflows taught during the workshop reflect 160 those commonly required in real-world projects involving clinical and laboratory datasets in 161 tabular/structured form. By focusing on broadly applicable methods rather than highly 

- 162 specialised implementations, participants are encouraged to directly map workshop content 163 to their own research or professional practice. 

- 164 Progressive scaffolding: The workshop follows a linear and cumulative structure, with each 165 session explicitly building on concepts and skills introduced in prior sessions. This 

- 166 progressive scaffolding supports participants with varying levels of prior experience, 167 enabling them to incrementally develop competence through guided practice. 

- 168 Reproducibility and transparency: The workshops are grounded in the principles of the 

- 169 scientific method, with reproducibility positioned as a central priority. Participants are 

- 170 introduced to best practices for structuring analytical workflows, documenting experimental 171 decisions, and reporting results in a transparent and trustworthy way. 

- 172 Experimentation and exploration: Participants are encouraged to actively experiment with 

- 173 the techniques introduced during the workshop, including applying them to their own 

- 174 datasets where feasible. This emphasis on exploration reflects experiential learning 

- 175 principles, reinforcing the iterative nature of ML and supporting deeper engagement with 

- 176 both methodological choices and their practical implications. 

- 177 Together, these design principles support the development of ML literacy by prioritising 178 conceptual understanding, critical thinking, and practical relevance over exhaustive technical 

- 179 detail, while remaining aligned with established theories of learning and instruction. 

- 180 **7.2 Workshop structure** 

- 181 The one-day workshops are structured to provide participants with fundamental background 182 knowledge in ML and data science, before spending the remainder of the workshop focusing 183 on the practical implementation and expression of these fundamentals. Collectively, we refer 184 to these practical components as “hands-on sessions”. The Original workshop in 2019 

- 185 designed and delivered by TI was the foundation for the design of the subsequent 186 workshops. The major difference between them is one of scope. In 2019, the focus of the 187 workshop was on applying _Orange_ specifically to antimicrobial susceptibility testing data. 

- 188 Following workshops designed by BM and TI focused on working with tabular datasets more 189 generally, as these are the types of datasets that practitioners are more likely to encounter 190 in their own environments. Most practitioners would also be familiar with tabular datasets. 191 The timeline for each of the workshops, along with the topic of each session is presented in 192 Table 1. 193 194 195 196 197 198 199 200 

201 

202 

## 203 



|2019<br>ECCMID<br>(time: topic)|2024<br>ECCMID<br>(time:<br>topic)|2025<br>ESCMID<br>Global<br>(time:<br>topic)|2025<br>Universit<br>y of<br>Zurich<br>(time:<br>topic)|2026 ESCMID<br>Global (time:<br>topic)|2026 University<br>of Zurich (time:<br>topic)|
|---|---|---|---|---|---|
|09:30:<br>Welcome|09:00:<br>Welcome,<br>Data<br>science<br>and<br>machine<br>learning<br>backgroun<br>d|09:00:<br>Welcome,<br>Data<br>science<br>and<br>machine<br>learning<br>backgroun<br>d|09:00:<br>Welcome<br>, Data<br>science<br>and<br>machine<br>learning<br>backgrou<br>nd|9:00 – 9:30:<br>Workshop<br>welcome/introdu<br>ction to data<br>science and<br>machine learning|9:00 – 9:30:<br>Workshop<br>welcome/introdu<br>ction to data<br>science and<br>machine learning|
|09:35:<br>Broad<br>principles of<br>machine<br>learning|10:00 –<br>10:45:<br>Hands on<br>session 1 –<br>Introducti<br>on to<br>Orange|10:00 –<br>10:45:<br>Hands on<br>session 1 –<br>Introducti<br>on to<br>Orange|10:00 –<br>10:45:<br>Hands on<br>session 1<br>–<br>Introduct<br>ion to<br>Orange|9:30 – 10:00:<br>Understanding<br>the “end-to-end<br>machine learning<br>lifecycle” and<br>hands on session<br>1– Introduction<br>to Orange|9:30 – 10:00:<br>Understanding<br>the “end-to-end<br>machine learning<br>lifecycle” and<br>hands on session<br>1 – Introduction<br>to Orange|
|10:00:<br>Introducing<br>open-source<br>machine<br>learning<br>software|10:45 –<br>11:15:<br>Morning<br>break|10:45 –<br>11:15:<br>Morning<br>break|10:45 –<br>11:15:<br>Morning<br>break|10:00 – 10:45:<br>Hands on session<br>2 - Data cleaning<br>and preparation|10:00 – 10:45:<br>Hands on session<br>2 - Data cleaning<br>and preparation|
|10:15: Step<br>1: Caring for<br>your data –|11:15 –<br>12:00:|11:15 –<br>12:00:|11:15 –<br>12:00:<br>Hands on|10:45 – 11:15:<br>Morning break|10:45 – 11:15:<br>Morning break|



|scraping<br>and<br>cleaning|Hands on<br>session 2 -<br>Data<br>cleaning<br>and<br>preparatio<br>n|Hands on<br>session 2<br>Data<br>cleaning<br>and<br>preparatio<br>n|session 2<br>- Data<br>cleaning<br>and<br>preparati<br>on|||
|---|---|---|---|---|---|
|10:45:<br>Morning<br>break|12:00 –<br>13:00:<br>Hands on<br>session 3 -<br>Training<br>machine<br>learning<br>models|12:00 –<br>13:00:<br>Hands on<br>session 3 -<br>Training<br>machine<br>learning<br>models|12:00 –<br>13:00:<br>Hands on<br>session 3<br>- Training<br>machine<br>learning<br>models|11:15 – 12:00:<br>Hands on session<br>3 - Training<br>machine learning<br>models|11:15 – 12:00:<br>Hands on session<br>3 - Training<br>machine learning<br>models|
|11:15: Step<br>2: Define<br>your control<br>population<br>with data<br>machine 1|13:00 –<br>14:00:<br>Lunch<br>break|13:00 –<br>14:00:<br>Lunch<br>break|13:00 –<br>14:00:<br>Lunch<br>break|12:00 – 13:00:<br>Hands on session<br>4 - Evaluating<br>machine learning<br>models|12:00 – 13:00:<br>Hands on session<br>4 - Evaluating<br>machine learning<br>models|
|12:00: Step<br>3: First look<br>AST with<br>data<br>machine 2|14:00 –<br>15:00<br>Hands on<br>session 4 -<br>Evaluating<br>machine<br>learning<br>models|14:00 –<br>15:00:<br>Hands on<br>session 4 -<br>Evaluating<br>machine<br>learning<br>models|14:00 –<br>15:00:<br>Hands on<br>session 4<br>and 5 -<br>Evaluatin<br>g<br>machine<br>learning<br>models<br>and<br>testing<br>our<br>models<br>with new<br>data and|13:00 – 14:00:<br>Lunch break|13:00 – 14:00:<br>Lunch break|



||||retraining<br>our<br>model|||
|---|---|---|---|---|---|
|13:00:<br>Lunch break<br>and<br>troubleshoo<br>ting|15:00 –<br>16:00:<br>Hands on<br>session 5 -<br>Testing<br>our<br>models<br>with new<br>data and<br>retraining<br>our model|15:00 –<br>16:00:<br>Hands on<br>session 5 -<br>Testing<br>our<br>models<br>with new<br>data and<br>retraining<br>our model|15:00 –<br>16:00<br>Hands on<br>session<br>6- More<br>machine<br>learning<br>workflow<br>examples|14:00 – 15:00:<br>Hands on session<br>5 - Testing our<br>models with new<br>data and<br>retraining our<br>model|14:00 – 15:00:<br>Hands on session<br>5 - Testing our<br>models with new<br>data and<br>retraining our<br>model<br>Hands on session<br>6 - More<br>machine learning<br>workflow<br>examples|
|14:00: Step<br>4: Closer<br>look at AST<br>with data<br>machine 3|16:00 –<br>17:00:<br>Hands on<br>session 6 -<br>More<br>machine<br>learning<br>workflow<br>examples|16:00 –<br>16:30:<br>hands on<br>session 6-<br>More<br>machine<br>learning<br>workflow<br>examples|16:00:<br>Question<br>s,<br>technical<br>assistanc<br>e, and<br>discussio<br>n.|15:00 – 16:00:<br>Hands on session<br>6 - More<br>machine learning<br>workflow<br>examples|15:00 – 16:00:<br>Guidance for<br>publishing<br>machine learning<br>research|
|15:00 Step<br>5: Create<br>your data<br>machine<br>ensemble|17:00 –<br>18:00:<br>Close<br>workshop<br>-<br>Opportuni<br>ties for<br>further<br>questions,<br>technical|16:30 –<br>17:00<br>Presentati<br>on by Tim<br>Inglis<br>regarding<br>applicatio<br>n of data<br>science<br>and||16:00 – 17:00:<br>Guidance for<br>publishing<br>machine learning<br>research and<br>presentation by<br>Tim Inglis<br>regarding<br>application of<br>data science and|16:00 – 17:00:<br>Close workshop -<br>Opportunities for<br>further<br>questions,<br>technical<br>assistance,<br>networking|



204 



||assistance,<br>networkin<br>g|machine<br>learning<br>for<br>infection<br>science<br>and<br>clinical<br>microbiolo<br>gy.|machine learning<br>for infection<br>science and<br>clinical<br>microbiology|
|---|---|---|---|
|15:30:<br>Summative<br>exercise||17:00 –<br>18:00:<br>Close<br>workshop<br>-<br>Opportuni<br>ties for<br>further<br>questions,<br>technical<br>assistance,<br>networkin<br>g|17:00 – 18:00:<br>Close workshop -<br>Opportunities for<br>further<br>questions,<br>technical<br>assistance,<br>networking|
|16:00:<br>Review||||



**Table 1: The timeline and topic of each session for the workshops presented in 2019,2024, 2025, and 2026** 

# 205 **8. Workshop implementation and delivery** 

## 206 **8.1 Workshop preparation** 

- 207 The workshops are taught using the _Orange_ data mining software. To ensure that the 

- 208 workshop is delivered efficiently, it is critical that participants are appropriately set up with 

- 209 _Orange_ on their own laptops before attending the workshop. To coordinate this, BM 

- 210 developed a brief instructional document to guide participants in installing _Orange_ on their 

- 211 own laptops. The instruction documents have been developed for Windows, Mac, and Linux 

- 212 (Ubuntu) operating systems. They are sent out to all participants as part of the pre-workshop 

- 213 communications strategy. This strategy, which ensures that participants are prepared for the 

- 214 workshop, is outlined in Table 2. Across all workshops, participants were appropriately set 

- 215 up when they arrived, demonstrating the effectiveness of this communication approach. 

- 216 The course material is also provided to participants, made available to them via a link to a 

- 217 password protected _Dropbox_ folder. The content remains available to participants beyond 

- 218 the conclusion of the workshop. 

- 219 The rooms used for the workshops are of a classroom style set up, with access to power at 

- 220 each individual desk so that participants can ensure their devices have sufficient battery 

- 221 power to sustain the activities throughout the duration of the workshop. 

222 

||Weeks until workshop|Email content|
|---|---|---|
||8|-<br>Facilitator introduction.<br>-<br>Summary of the content in the<br>workshop.<br>-<br>Instructions for installing _Orange._|
||4|-<br>Sharing the Dropbox link that<br>contains all the workshop material.<br>-<br>Sharing the schedule for the<br>workshop.<br>-<br>Instructions for participants to bring<br>their own datasets if they are<br>interested.|
||1|-<br>Reminder of start time of the<br>workshop and details regarding<br>venue.<br>-<br>Reminders regarding accessing the<br>content and downloading the<br>_Orange _software.|
|223<br>224|**Table 2: Due to the international nature of the workshop, ema**<br>**sent 8, 4, and 1 week before the workshop, with each email co**|**il is used to communicate with participants. Emails are**<br>**ntaining content to support appropriate participant**|



- 225 **preparation** 

## 226 **8.2 Workshop delivery** 

- 227 The workshop content is typically taught by both BM and TI. BM delivers the session 

- 228 content, both theoretical and hands-on sessions, with TI providing technical support and 

- 229 clinical microbiology expertise. Having a professional data scientist (BM) and a clinical 

- 230 microbiologist (TI) delivering the workshop allows for a more diverse range of skill sets and 

- 231 knowledge to support participants with their questions and inquiries. Both BM and TI acted 

- 232 as coaches during the hands-on sessions, modelling the content to participants and 

- 233 demonstrating reasoning and transparent problem-solving practices. Participants are 

- 234 encouraged to ask questions and participate throughout the hands-on sessions. The break 

- 235 periods, as shown in Table 1, provide opportunities for students to consolidate what they 

- 236 have learnt, ask questions, receive technical support, or have a rest before starting the next 237 set of sessions. 

## 238 

## 239 **8.3 Session content** 



- 240 **8.3.1 Introductory presentation** 

- 241 The workshops start with a one-hour presentation. This presentation consists of a general 242 introduction to the workshop and outlines the learning goals. Participants are shown the 243 final _Orange_ workflow that they build by the conclusion of the workshop (Figure 1). The 

- 244 workflow that participants build is based on previous work by BM, TI, and MR, regarding ML 245 for blood culture outcome prediction [13]. To the best of our knowledge, this is the first time 

- 246 that a workshop has been delivered that presents a workflow for blood culture outcome 

- 247 prediction. However, the workflows can be easily adapted, and participants are encouraged 248 to bring their own datasets to the workshop and apply what they learn to their specific 249 problems. Following this introduction, for the remaining hour of the first session, we cover 

- 250 fundamental data science, and ML concepts, and provide some examples of where ML has 251 been applied to infectious diseases and clinical microbiology. Following this, we introduce 252 the data science and ML lifecycle to participants, outlining the main components, including 

- 253 1) problem identification and ML objective; 2) data preparation; 3) model development; and 254 4) evaluation. We then provide additional background on structured data and supervised 255 ML. 

## 256 

- 257 {{TYPE:image; FILENAME:image1.png; ID:rId13}} 

- 258 **Figure 1: Final analytical workflow developed by the participants of the workshop. Includes data cleaning and** 

- 259 **processing, training and testing machine learning models, cross-validation, and model evaluation.** 

- 260 

- 261 

- 262 



- 263 **8.3.2 Hands-on session 1** 264 The first hands-on session is designed to introduce participants to the _Orange_ software 265 ecosystem in preparation for the remainder of the workshop. The session utilises publicly 266 available, published data [14], and its focus is on how to use _Orange_ . This includes importing 267 data into the application and visualising it. The resulting workflow produced during this 268 hands-on session is shown in Figure 2. 

## 269 {{TYPE:image; FILENAME:image2.png; ID:rId14}} 

- 270 **Figure 2: Workflow that participants build during the first hands-on session. Participants learn how to import data,** 271 **visualise it in a table, and perform exploratory data analysis. The purpose of this session is to show participants how to** 272 **use the Orange software.** 

## 273 

## 274 **8.3.3 Hands-on session 2** 

- 275 Following the first break, we start with hands-on session 2. This is the first hands-on session 276 that involves the BC outcome prediction use case. The focus of this session is data cleaning 277 and preparation for ML modelling. The session starts with importing the data, followed by 

- 278 participants learning how to filter data, create new columns/features, and select 

- 279 columns/features, before concluding with the training and test data split. The focus of this 

- 280 session is for participants to understand how to prepare tabular datasets for ML and 

- 281 highlight the importance of the training and test split. The workflow produced during this 282 session is shown in Figure 3. 

## 283 

- 284 {{TYPE:image; FILENAME:image3.png; ID:rId15}} 

- 285 **Figure 3: In hands-on session 2, participants focus on data cleaning and preparation for machine learning. Starting with** 286 **importing the data and concluding with the creation of training and test datasets.** 

## 287 

## 288 **8.3.4 Hands-on session 3** 

- 289 Hands-on session 3 introduces the ML training and cross-validation process. We discuss the 290 importance of cross-validation and why it is a critical component of any ML pipeline. For the 

- 291 modelling, we start with tree-based models and explain the importance of model 

- 292 hyperparameters. As hands-on session 2 and hands-on session 3 are both in-depth sessions, 

- 293 they are followed by a one-hour break. The workflow produced by the end of hands-on 294 session 3 is shown in Figure 4. 

## 295 

- 296 {{TYPE:image; FILENAME:image4.png; ID:rId16}} 297 **Figure 4: In hands-on session 3, participants focus on the training of machine learning models, building on the previous** 298 **session.** 

- 299 **8.3.5 Hands-on session 4** 300 Hands-on session 4 focuses on the evaluation of ML models. An entire session is dedicated 301 to this topic, as it is very important for those aiming to develop their own ML models and 

- 302 those reviewing ML models developed by others. Performance metrics can be misleading in 

- 303 the context of highly imbalanced datasets, such as the one participants use in the 

- 304 workshops, and this is discussed in detail. In this session, we primarily focus on the area 

- 305 under the receiver operating characteristic curve (AUC), and metrics relating to the 

- 306 confusion matrix such as sensitivity and specificity. We also build on the previous session to 307 go beyond training and cross-validation performance and examine model performance on 

- 308 the test set we prepared earlier. The workflow produced by the end of this session is shown 309 in Figure 5. 

310 

- 311 {{TYPE:image; FILENAME:image5.png; ID:rId17}} 

- 312 **Figure 5: Hands-on session 4 focuses on evaluating the models trained in the previous session. This includes evaluating** 313 **the models during cross-validation and assessing their performance on the test set.** 

## 314 **8.3.6 Hands-on session 5** 

- 315 Hands-on session 5 focuses on the example case of using an external validation set and how 

- 316 participants can adapt their workflow to accommodate this. By the end of this session, 

- 317 participants have completed the entire BC outcome prediction workflow (Figure 1). Likewise, 

- 318 participants using their own datasets should have a similar workflow adapted to their 319 particular purpose. 

## 320 

## 321 **8.3.7 Hands-on session 6** 

- 322 Hands-on session 6 extends on what participants have learnt over the course of the 

- 323 workshop and introduces some different types of workflows. These include workflows 

- 324 where more data cleaning is required, such as missing value handling and encoding of 

- 325 categorical variables. Multiclass classification is also discussed. Additional workflows for 326 regression tasks, unsupervised learning, and computer vision are also introduced. 

- 327 

- 328 All participants receive the workshop materials before the workshop, and the content 

- 329 remains available to them after it concludes. Participants are provided with a record of all 

- 330 email communication, instructions for installing the _Orange_ software, the workshop 

- 331 presentation slides, copies of the completed _Orange_ workflows, and additional 

- 332 supplementary material, including the datasets. 

- 333 

- 334 

- 335 

# 336 **9.  Reflections** 

- 337 After delivering this workshop on multiple occasions to a diverse audience, there is a clear 

- 338 opportunity for reflection. Participants have come from a wide range of backgrounds, 

- 339 including medical microbiology, infectious diseases, laboratory science, epidemiology, data 

- 340 science, and graduate programmes. Designing and delivering a workshop that is valuable 

- 341 across such disciplinary diversity is challenging. This diversity is a key motivator for 

- 342 presenting the material in the most generalisable way possible, with an emphasis on shared 

- 343 concepts, workflows, and decision-making processes rather than on discipline-specific 344 technical detail. 

- 345 Levels of engagement varied across the range of participants, reflecting both differences in 

- 346 prior experience and the intensity of the material. A recurring challenge is the risk of 

- 347 information overload. While the one-day format is beneficial in enabling efficient content 

- 348 delivery, it is also inherently constrained. There is a practical limit to the depth achievable in 

- 349 a single day, and depth is often sacrificed in favour of conceptual coherence. The primary 

- 350 objective of the workshop, therefore, is not complete technical mastery, but rather for 

- 351 participants to leave with robust mental models of the ML lifecycle, alongside introductory 

- 352 technical skills and improved literacy. 

- 353 This trade-off is an acknowledged limitation of the one-day format. The contrast became 

- 354 particularly evident during delivery of a multi-day version of the workshop, in which content 

- 355 could be distributed across several days [5]. In this setting, concepts were reinforced 

- 356 iteratively, allowing participants more time to reflect, consolidate learning, and build 

- 357 progressively on prior material. Additionally, the workshop is delivered exclusively in English, 

- 358 which may limit accessibility for participants whose primary language is not English. 

- 359 **10. Future directions** 

- 360 Across all workshops delivered in 2024, 2025, and 2026, the material has been taught to 220 

- 361 participants from a range of countries and professional backgrounds. There are plans to 362 continue offering this workshop in future years if demand remains. Beyond in-person 363 delivery, a key future objective is to ensure that the workshop material is accessible to the 364 wider infection science community. In support of this goal, an open-source repository will be 365 created to host the workshop and supplementary content. The repository will serve as a 

- 366 freely available, regularly updated educational resource for those interested in applying 

- 367 machine learning to infection science. Its open-source nature will enable community 368 contribution, adaptation, and extension, including a roadmap for future development. 

- 369 Participant feedback was collected following workshop delivery and provided valuable 

- 370 insights into potential improvements. However, ethics approval was not obtained to formally 

- 371 analyse or report this feedback; therefore, it is not included in this paper. Future research 

- 372 ethics-approved work may enable systematic evaluation of participant feedback and its use 

- 373 in future reports. 

- 374 While quantitative and qualitative feedback is important for evaluating the success of 

- 375 educational initiatives, broader indicators of impact should also be considered. Reflections, 

- 376 such as whether participants became more critical consumers of ML literature or whether 

- 377 new collaborations and projects emerged following the workshop, may provide more 

- 378 meaningful insight into the workshop’s achievement of its intended objectives. 

- 379 Although the one-day workshop format is efficient and effective practical introduction to the 

- 380 ML lifecycle, it does not scale infinitely. There is a finite amount of material that can be 

- 381 reasonably accommodated within the current structure. Multi-day formats are better suited 

- 382 to spaced repetition, deeper exploration of complex topics, and more sustained 

- 383 engagement. Expanding the delivery format represents an important area for future 

- 384 development. For example, the workshop could be delivered online across multiple shorter 

- 385 sessions, improving accessibility and reducing resource requirements associated with in- 

- 386 person attendance. 

- 387 Finally, given the multidisciplinary nature of the participant cohort, the workshop provides a 

- 388 valuable opportunity for networking and collaboration. Future iterations should place 

- 389 greater emphasis on facilitating interaction and collaboration among participants as a core 

- 390 component of the workshop design. We hope that this paper will encourage other educators 

- 391 to develop similar workshops based on the framework presented here, thereby supporting 

- 392 broader efforts to improve ML literacy within the infection science community. 

- 393 **11. Conclusion** 

- 394 The _“Using Data Science and Machine Learning for Infection Science: A Hands-On_ 

- 395 _Introduction”_ workshops demonstrate how carefully designed, one-day educational 

- 396 interventions can support development of computational literacy among infection science 

- 397 professionals, while maintaining a commitment to transparency and open science. By 

- 398 integrating foundational theory of the ML lifecycle with real-time demonstrations and 

- 399 hands-on sessions, the workshop offers a replicable model for domain-specific data science 400 education. 

- 401 Successful delivery of the workshop on multiple occasions suggests that this approach is 402 both feasible and valuable for the infection science and clinical microbiology community. As 403 the workshop continues to evolve, ongoing reflection is needed to identify opportunities for 404 improvement, expansion, and broader dissemination of the material. By sharing both the 

- 405 content and lessons learned through open channels, we hope that this work will become a 

- 406 blueprint for similar educational initiatives and contribute to more informed, critical, and 407 responsible use of ML in infection science and clinical microbiology. 

- 408 

## 409 

- 410 **12. Author statements** 

- 411 **12.1 Author contributions** 



- 412 BM wrote the initial draft of this manuscript and designed and delivered the workshops in 413 2024, 2025, and 2026. TI reviewed the manuscript, provided editorial support, and 

- 414 supervision. TI designed and delivered the 2019 workshop, mentioned in this paper. TI was 

- 415 also present at the ECCMID and ESCMID Global workshops in 2024, 2025, and 2026 to 416 provide technical assistance for participants. MR provided editorial support. 

## 417 

- 418 **12.2 Conflicts of interest** 

- 419 The author(s) declare that there are no conflicts of interest. 

- 420 **12.3 Funding information** 

- 421 For the workshops in Zurich, travel and accommodation costs were covered by the 422 University of Zurich. BM and TI received waivers of conference registration fees at 423 ECCMID/ESCMID Global. 

- 424 **12.4 Ethical approval** 

- 425 Not applicable 

- 426 **12.5 Consent for publication** 

- 427 Not applicable 

- 428 **12.6 Acknowledgements** 429 The authors would like to thank Carla Seiler and the ESCMID Global organising team for their 430 support in organising the workshops in 2024, 2025, and 2026. We would also like to thank 431 Karolyn Moore for helping to organise the 2026 ESCMID Global workshop. We would also 432 like to thank Professor Adrian Egli and Birke Mebold for helping to organise the workshop at 433 the University of Zurich in 2025 and 2026. Lab without walls supported BM with funding for 434 flights and accommodation in 2024 to attend the ECCMID conference in Barcelona and 435 deliver the workshop. BM was supported by an Australian Government Research Training 436 Program (RTP) Scholarship. 

## 437 

- 438 **13. References** 



- 439 [1]- Luz CF, Vollmer M, Decruyenaere J, Nijsten MW, Glasner C, Sinha B. Machine learning in 

- 440 infection management using routine electronic health records: tools, techniques, and 441 reporting of future technologies. Clinical Microbiology and Infection. 2020 Oct 442 1;26(10):1291-9. 

- 443 [2] - Vercio LL, Amador K, Bannister JJ, Crites S, Gutierrez A, MacDonald ME, Moore J, 

- 444 Mouches P, Rajashekar D, Schimert S, Subbanna N. Supervised machine learning tools: a 

- 445 tutorial for clinicians. Journal of Neural Engineering. 2020 Nov 19;17(6):062001. 

- 446 [3] - Magnano CS, Mu F, Russ RS, Cvetkovic M, Treu D, Gitter A. An approachable, flexible and 

- 447 practical machine learning workshop for biologists. Bioinformatics. 2022 Jul 

- 448 1;38(Supplement_1):i10-8. 

- 449 [4] - Demsar J, Curk T, Erjavec A, Gorup C, Hocevar T, Milutinovic M, Mozina M, Polajnar M, 

- 450 Toplak M, Staric A, Stajdohar M, Umek L, Zagar L, Zbontar J, Zitnik M, Zupan B 

- 451 (2013) Orange: Data Mining Toolbox in Python, _Journal of Machine Learning_ 

- 452 _Research_ 14(Aug): 2349−2353. 

- 453 [5] - Mariella Greutmann, Karsten Borgwardt, Sarah Brüningk, Fabian Franzeck, Christian G. 

- 454 Giske, Anna G. Green, Alejandro Guerrero-López, Margaret Ip, Catherine Jutzeler, Andre 

- 455 Kahles, Michael Krauthammer, Nenad Macesic, Benjamin McFadden, Eline Meijer, Nathan 

- 456 Moore, Jacob Moran-Gilad, Imane Lboukili, Oliver Nolte, Robin Patel, Gerold Schneider, 

- 457 Markus A. Seeger, Tavpritesh Sethi, Robert L. Skov, Chang Ho Yoon, Belén Rodríguez-Sánchez, 

- 458 Adrian Egli,ESCMID workshop: Artificial intelligence and machine learning in medical 

- 459 microbiology diagnostics, Microbes and Infection, 2025, 105562, ISSN 1286-4579, 

- 460 https://doi.org/10.1016/j.micinf.2025.105562. 

- 461 (https://www.sciencedirect.com/science/article/pii/S1286457925000942) 

- 462 [6] - McFadden BR, Reynolds M, Inglis TJ. Developing machine learning systems worthy of 463 trust for infection science: a requirement for future implementation into clinical practice. 464 Frontiers in Digital Health. 2023 Sep 27;5:1260602. 

- 465 [7] - Goktas P, Grzybowski A. Shaping the future of healthcare: ethical clinical challenges and 466 pathways to trustworthy AI. Journal of Clinical Medicine. 2025 Feb 27;14(5):1605. 

- 467 [8] - Bürger VK, Amann J, Bui CK, Fehr J, Madai VI. The unmet promise of trustworthy AI in 468 healthcare: why we fail at clinical translation. Frontiers in Digital Health. 2024 Apr 469 18;6:1279629. 

- 470 [9] - Fehr J, Citro B, Malpani R, Lippert C, Madai VI. A trustworthy AI reality-check: the lack of 471 transparency of artificial intelligence products in healthcare. Frontiers in Digital Health. 2024 

- 472 Feb 20;6:1267290. 

- 473 [10] - Biggs J, Tang C, Kennedy G. Teaching for quality learning at university 5e. McGraw-hill 474 education (UK); 2022 Nov 2. 

- 475 [11] - Kolb DA. Experiential learning: Experience as the source of learning and development. 476 FT press; 2014 Dec 17. 

- 477 [12] - Collins A, Brown JS, Newman SE. Cognitive apprenticeship: Teaching the crafts of 

- 478 reading, writing, and mathematics. InKnowing, learning, and instruction 2018 Dec 7 (pp. 479 453-494). Routledge. 

- 480 <u>[13] -</u> McFadden BR, Inglis TJ, Reynolds M. Machine learning pipeline for blood culture 

- 481 outcome prediction using Sysmex XN-2000 blood sample results in Western Australia. BMC 

- 482 infectious diseases. 2023 Aug 24;23(1):552. 

- 483 [14] - Oonsivilai M, Mo Y, Luangasanatip N, Lubell Y, Miliya T, Tan P, Loeuk L, Turner P, Cooper 

- 484 BS. Using machine learning to guide targeted and locally-tailored empiric antibiotic 

- 485 prescribing in a children's hospital in Cambodia. Wellcome open research. 2018 Oct 486 10;3:131. 



