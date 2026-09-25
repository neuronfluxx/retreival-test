<!-- Extracted using strategy: text -->

|As|hish|Vaswani|∗|Col5|Noam Shazeer|∗|Niki Parmar∗|Jakob Uszkorei|t∗|
|---|---|---|---|---|---|---|---|---|---|
|G|oog|le Brain|||Google Brain|G|oogle Research|Google Researc|h|
|`avasw`|`ani`|`@google.`|`c`|`om`<br>`no`|`am@google.c`|`om`<br>`ni`|`kip@google.com`|`usz@google.co`|`m`|
|||||||||||
||**Llio**|**n Jones**_∗_|||**Aidan N. G**|**  omez**_∗†_|**Łuka**|**sz Kaiser**_∗_||
|G|oogl|e Research|||University of|Toronto|Goo|gle Brain||
|`lli`|`on@`|`google.c`|`o`|`m`<br>`a`|`idan@cs.tor`|`onto.ed`|`u`<br>`lukaszkais`|`er@google.com`||
|||||||||||
||||||**Illia Po**|** losukhin**|_∗‡_|||
|||||`i`<br>|<br>`llia.polosu`<br>**Ab**<br>|<br>`khin@gm`<br>**stract**<br>|`ail.com`<br>|||
||The|dominant|s|equence|transduction|models ar|e based on complex|recurrent or||
||con|volutional|n|eural net|works that inc|lude an e|ncoder and a deco|der. The best||
||perf|orming m|o|dels also|connect the e|ncoder a|nd decoder through|an attention||
||mec|hanism.|W|e propos|e a new simp|le networ|k architecture, the|Transformer,||
||base|d solely on||attention|mechanisms, d|ispensing|with recurrence and|convolutions||
||enti|rely. Exp|er|iments o|n two machin|e transla|tion tasks show the|se models to||
||be s|uperior in|q|uality w|hile being mor|e parallel|izable and requiring|signiﬁcantly||
||less|time to tr|ai|n. Our|model achieve|s 28.4 BL|EU on the WMT 2|014 English-||
||to-G|erman tra|n|slation t|ask, improving|over th|e existing best resul|ts, including||
||ense|mbles, by|o|ver 2 BL|EU. On the W|MT 2014|English-to-French tr|anslation task,||
||our|model esta|bl|ishes a n|ew single-mod|el state-o|f-the-art BLEU scor|e of 41.0 after||
||train|ing for 3.|5|days on|eight GPUs, a|small fra|ction of the trainin|g costs of the||
||best|models fr|o|m the lite|rature.|||||
|<br><br>|<br>|<br>||||||||
|**1**<br>**Intr**|**od**|**uction**||||||||
|||||||||||
|Recurren|t ne|ural netwo|r|ks, long|short-term me|mory [12|] and gated recurre|nt [7] neural netwo|rks|
|in partic|ular,|have been|ﬁ|rmly es|tablished as sta|te of the|art approaches in se|quence modeling|and|
|transduct|ion|problems|s|uch as la|nguage model|ing and|machine translation|[29, 2, 5]. Numer|ous|
|efforts ha|ve s|ince contin|u|ed to pus|h the boundari|es of recur|rent language mode|ls and encoder-deco|der|
|architect|ures|[31, 21, 1|3]|.||||||
|<br>|<br>|<br>|<br>|<br>||||||
|_∗_Equal|con|tribution. Li|st|ing order|is random. Jako|b proposed|replacing RNNs with|self-attention and sta|rted|
|the effort|to ev|aluate this i|d|ea. Ashis|h, with Illia, des|igned and|implemented the ﬁrst|Transformer models|and|
|has been c|rucia|lly involved|i|n every as|pect of this work|. Noam pr|oposed scaled dot-pro|duct attention, multi-|head|
|attention|and t|he paramet|er|-free posi|tion representati|on and be|came the other person|involved in nearly e|very|
|detail. Ni|ki de|signed, imp|le|mented, t|uned and evalua|ted countle|ss model variants in o|ur original codebase|and|
|tensor2ten|sor.|Llion also e|x|perimente|d with novel mo|del varian|ts, was responsible for|our initial codebase,|and|
|efﬁcient in|fere|nce and visu|a|lizations.|Lukasz and Aida|n spent co|untless long days desig|ning various parts of|and|
|implemen|ting t|ensor2tenso|r,|replacing|our earlier code|base, great|ly improving results a|nd massively accelera|ting|
|our resear<br>|ch.<br>|||||||||
|_†_Work<br>|perf<br>|ormed whil<br>|e<br>|at Google<br>|Brain.<br>|||||
|_‡_Work|perf|ormed whil|e|at Google|Research.|||||
|<br>|<br>|<br>|<br>|<br>|<br>|||||
|31st Conf|eren|ce on Neura|l|Informati|on Processing S|ystems (NI|PS 2017), Long Beac|h, CA, USA.||

