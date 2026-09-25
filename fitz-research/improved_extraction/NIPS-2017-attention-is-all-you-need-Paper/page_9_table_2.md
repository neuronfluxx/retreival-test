<!-- Extracted using strategy: text -->

|Table 3: Variations on the Transf|o|rme|r ar|chi|tecture. Un|listed values|are ide|ntical to those of the base|
|---|---|---|---|---|---|---|---|---|
|model. All metrics are on the En|g|lish|-to|-Ge|rman trans|lation develo|pment|set, newstest2013. Listed|
|perplexities are per-wordpiece, a|c|cor|din|g to|our byte-p|air encoding|, and sh|ould not be compared to|
|per-word perplexities.|||||||||
||||||||||
|||||||tr|ain|PPL<br>BLEU<br>params|
||||||||||
|_N_<br>_d_model<br>_d_ff<br>|||_dk_||_dv_<br>_Pdr_|_op_<br>_ϵls_<br>||6|
|||||||st|eps<br>|dev)<br>(dev)<br>_×_10|
|base<br>6<br>512<br>2048|8||64||64<br>0.1|0.1<br>10|0K<br>|4.92<br>25.8<br>65|
||1||512||512|||5.29<br>24.9|
|(A)|4||128||128|||5.00<br>25.5|
||1|6|32||32|||4.91<br>25.8|
||3|2|16||16|||5.01<br>25.4|
||||16|||||5.16<br>25.1<br>58|
|(B)|||32|||||5.01<br>25.4<br>60|
|2||||||||6.11<br>23.7<br>36|
|4||||||||5.19<br>25.3<br>50|
|8||||||||4.88<br>25.5<br>80|
|(C)<br>256|||32||32|||5.75<br>24.5<br>28|
|1024|||128||128|||4.66<br>26.0<br>168|
|1024||||||||5.12<br>25.4<br>53|
|4096||||||||4.75<br>26.2<br>90|
||||||0.0|||5.77<br>24.6|
||||||0.2|||4.95<br>25.5|
|(D)||||||0.0||4.67<br>25.3|
|||||||0.2||5.47<br>25.7|
|(E)<br>positional emb|e|ddi|ng i|nst|ead of sinu|soids||4.92<br>25.7|
|big<br>6<br>1024<br>4096<br>|1|6|||0.3|30|0K<br>|**4.33**<br>**26.4**<br>213|
||||||||||
|In Table 3 rows (B), we observ|e|that|re|duc|ing the att|ention key si|ze_ dk_ h|urts model quality. This|
|suggests that determining com|p|atib|ilit|y is|not easy|and that a m|<br>ore so|phisticated compatibility|
|function than dot product may be||bene|ﬁc|ial.|We further|observe in ro|ws (C)|and (D) that, as expected,|
|bigger models are better, and dro|p|out i|s v|ery|helpful in a|voiding over-|ﬁtting.|In row (E) we replace our|
|sinusoidal positional encoding w|i|th l|ear|ned|positional|embeddings [|8], and|observe nearly identical|
|results to the base model.|||||||||
|<br><br>|||||||||
|**7**<br>**Conclusion**|||||||||
||||||||||
|In this work, we presented the T|r|ansf|orm|er,|the ﬁrst se|quence trans|duction|model based entirely on|
|attention, replacing the recurren|t|laye|rs|mos|t commonl|y used in enc|oder-d|ecoder architectures with|
|multi-headed self-attention.|||||||||
|<br>|||||||||
|For translation tasks, the Trans|f|orm|er c|an|be trained|signiﬁcantly|faster|than architectures based|
|on recurrent or convolutional l|a|yers|.|On|both WMT|2014 Engli|sh-to-G|erman and WMT 2014|
|English-to-French translation ta|s|ks,|we|ac|hieve a new|state of the|art. In|the former task our best|
|model outperforms even all prev|i|ousl|y r|epo|rted ensem|bles.|||
|<br>|<br>|<br>|<br>|<br>|<br>|<br>|||
|We are excited about the future|of|att|enti|on-|based mod|els and plan t|o appl|y them to other tasks. We|
|plan to extend the Transformer t|o|pro|ble|ms|involving i|nput and outp|ut mod|alities other than text and|
|to investigate local, restricted a|tt|enti|on|me|chanisms t|o efﬁciently|handle|large inputs and outputs|
|such as images, audio and video.||Mak|ing|ge|neration le|ss sequential|is anoth|er research goals of ours.|
|<br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>|
|The code we used to train a|n|d ev|alu|ate|our mod|els is availa|ble at|`https://github.com/`|
|`tensorflow/tensor2tensor`.<br>|||||||||
|**Acknowledgements**<br>We are g|r|atef|ul t|o N|al Kalchb|renner and S|tephan|Gouws for their fruitful|
|comments, corrections and inspi|r|atio|n.||||||

