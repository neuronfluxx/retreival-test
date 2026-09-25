<!-- Extracted using strategy: text -->

|Table 2: The Transf|ormer a|chieves better BL|EU scores|than prev|ious|state-of-the-|art models on the|
|---|---|---|---|---|---|---|---|
|English-to-German|and En|glish-to-French ne|wstest201|4 tests at|a fra|ction of the tr|aining cost.|
||||<br>|<br>||<br>|<br>|
||||BLE|U||Training Cos|t (FLOPs)|
|Model||||||<br>|<br>|
||||EN-DE<br>|EN-FR||EN-DE|EN-FR|
|ByteNet [15]|||23.75|||||
|Deep-Att + P|osUnk|[32]||39.2|||1_._0_ ·_ 1020<br>|
|GNMT + RL|[31]||24.6|39.92||2_._3_ ·_ 1019<br><br><br>|1_._4_ ·_ 1020<br>|
|ConvS2S [8]|||25.16|40.46||9_._6_ ·_ 1018<br><br><br>|1_._5_ ·_ 1020<br>|
|MoE[26]|||26.03|40.56||2_._0_ ·_ 1019<br>|1_._2_ ·_ 1020|
|Deep-Att + P|osUnk|Ensemble [32]||40.4|||8_._0_ ·_ 1020<br>|
|GNMT + RL|Ensem|ble [31]|26.30|41.16||1_._8_ ·_ 1020<br><br><br>|1_._1_ ·_ 1021<br>|
|ConvS2S En|semble|[8]|26.36|**41.29**||7_._7_ ·_ 1019<br>|1_._2_ ·_ 1021|
|Transformer|(base m|odel)|27.3|38.1||**3****_._3****_ ·_ 1**<br>|** 018**<br>|
|Transformer|(big)||**28.4**|**41.0**||2_._3_ ·_ 1|019|
||<br>|||||||
|**Label Smoothing**|Durin|g training, we em|ployed lab|el smoot|hing|of value_ ϵls_|= 0_._1 [30]. This|
|hurts perplexity, as t|he mod|el learns to be mo|re unsure,|but impr|oves|<br>            accuracy and|BLEU score.|
|<br><br>||||||||
|**6**<br>**Results**||||||||
|||||||||
|**6.1**<br>**Machine Tra**|** nslation**|||||||
|<br>|<br>|<br>||||||
|On the WMT 2014|English|-to-German transla|tion task, t|he big tra|nsfo|rmer model (|Transformer (big)|
|in Table 2) outperfo|rms the|best previously re|ported mo|dels (incl|udin|g ensembles)|by more than 2_._0|
|BLEU, establishing|a new|state-of-the-art B|LEU score|of 28_._4.|The|conﬁguration|of this model is|
|listed in the bottom|line of|Table 3. Training|took 3_._5 d|ays on 8|P10|0 GPUs. Eve|n our base model|
|surpasses all previo|usly pu|blished models an|d ensemble|s, at a fra|ctio|n of the traini|ng cost of any of|
|the competitive mod|els.|||||||
|<br>|<br>|||||||
|On the WMT 2014|English|-to-French translat|ion task, o|ur big mo|del|achieves a BL|EU score of 41_._0,|
|outperforming all of|the pre|viously published|single mo|dels, at le|ss t|han 1_/_4 the tr|aining cost of the|
|previous state-of-th|e-art m|odel. The Transfo|rmer (big)|model t|rain|ed for Englis|h-to-French used|
|dropout rate_ Pdrop_|= 0_._1, i|nstead of 0_._3.||||||
|<br>|<br>|<br>||||||
|For the base model|s, we us|ed a single mode|l obtained|by avera|ging|the last 5 ch|eckpoints, which|
|were written at 10-|minute|intervals. For the|big model|s, we ave|rage|d the last 20|checkpoints. We|
|used beam search w|ith a b|eam size of 4 and|length pen|alty_ α_ =|0_._6|[31]. These|hyperparameters|
|were chosen after ex|perime|ntation on the deve|lopment se|t. We set|the|maximum out|put length during|
|inference to input le|ngth +|50, but terminate e|arly when|possible|[31|].||
|<br>|<br>|<br>|<br>|<br>|<br>|<br>||
|Table 2 summarizes|our res|ults and compares|our translat|ion quali|ty a|nd training co|sts to other model|
|architectures from t|he litera|ture. We estimate|the numbe|r of ﬂoat|ing|point operatio|ns used to train a|
|model by multiplyin<br>|g the tr<br>|aining time, the n<br>|umber of G<br>|PUs use|d, a|nd an estimat|e of the sustained|
|single-precision ﬂoa|ting-po|int capacity of eac|h GPU 5.|||||
|<br><br>|<br>|||||||
|**6.2**<br>**Model Variat**|** ions**|||||||
|<br>|<br>|||||||
|To evaluate the imp|ortance|of different comp|onents of|the Trans|for|mer, we varie|d our base model|
|in different ways, m|easuri|ng the change in p|erformanc|e on Eng|lish|-to-German t|ranslation on the|
|development set, ne|wstest2|013. We used bea|m search|as descri|bed|in the previou|s section, but no|
|checkpoint averagin|g. We|present these resul|ts in Table|3.||||
|<br>|<br>|<br>|<br>|<br>||||
|In Table 3 rows (A),|we vary|the number of atte|ntion head|s and the|atte|ntion key and|value dimensions,|
|keeping the amoun|t of co|mputation constan|t, as desc|ribed in|Sect|ion 3.2.2. W|hile single-head|
|attention is 0.9 BLE|U wors|e than the best set|ting, qualit|y also dr|ops|off with too m|any heads.|
|<br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>|
|5We used values o|f 2.8, 3.7|, 6.0 and 9.5 TFLO|PS for K80,|K40, M4|0 and|P100, respecti|vely.|

