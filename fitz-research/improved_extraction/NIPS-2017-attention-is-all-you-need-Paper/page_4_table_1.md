<!-- Extracted using strategy: text -->

|Figure 2: (|le|ft) Scal|ed Do|t-Product|Attenti|on. (rig|ht) Multi|-Head Attenti|on cons|ists of several|
|---|---|---|---|---|---|---|---|---|---|---|
|attention la|ye|rs runni|ng in|parallel.|||||||
|<br>|<br>|<br>|<br>|<br> _√_|||||||
|query with|al|l keys, d|ivide|each by|_dk_, and|apply a|softmax|function to obt|ain the|weights on the|
|<br>values.<br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>|
|In practice,|w|e comp|ute th|e attention|functi|on on a s|et of que|ries simultane|ously, pa|cked together|
|into a matri|x|_ Q_. The|keys|and values|are als|o packed|together|into matrices|_ K_ and_ V_|. We compute|
|the matrix o|f|outputs|as:||||||||
|||||||||_QKT_<br>|||
|||||Attentio|n(_Q, K_|_ , V_ ) = s|oftmax(|~~_√_~~<br>)_V_||(1)|
|||||||||_dk_<br>|||
|The two mo|st|comm|only u|sed attenti|on func|tions are|additive|attention [2], a|nd dot-p|roduct (multi-|
|plicative) at<br>|te|ntion. D|ot-pr|oduct atten|tion is|identical|to our al|gorithm, excep|t for the|scaling factor|
|of<br>1<br>~~_√_~~_d_ . Ad|di|tive atte|ntion|computes|the com|patibilit|y functio|n using a feed-|forward|network with|
|_k_   <br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>|
|<br>a single hid|d|en layer|. Whi|le the two|are sim|ilar in th|eoretical|complexity, d|ot-produ|ct attention is|
|much faster|a|nd more|space|-efﬁcient i|n pract|ice, since|it can be|implemented|using hig|hly optimized|
|matrix mult|ip|lication|code.||||||||
|<br>|<br>|<br>|<br>|<br>|||||||
|While for s|m|all value|s of_ d_|_k_ the two|mechan|isms per|form sim|ilarly, additive|attentio|n outperforms|
|dot product|a|ttention|witho|<br>   ut scaling|for larg|er values|of_ dk_ [3|]. We suspect t|hat for l|arge values of|
|_dk_, the dot<br>|pr<br>|oducts g<br>|row l<br>|arge in ma<br>|gnitude,<br>|pushing<br>|<br>         the softm<br>|ax function in<br>|to regio<br><br>|ns where it has<br>|
|extremely s|m|all grad|ients 4|. To count|eract th|is effect,|we scale|the dot produ|cts by<br><br>~~_√_~~|1<br>_d_ .|
|<br><br>|<br>|<br>|<br>|<br>|||||<br>|_k_|
|**3.2.2**<br>**Mul**|**ti**|**-Head**|** Atten**|** tion**|||||||
|<br>|<br>|<br>|<br>|<br>|||||||
|Instead of p|e|rformin|g a sin|gle attenti|on func|tion with|_ d_model-d|imensional ke|ys, valu|es and queries,|
|we found it|b|eneﬁcia|l to lin|early proj|ect the|queries, k|eys and|values_ h_ times|with dif|ferent, learned|
||||||||||||
|linear proje|ct|ions to|_k_,_ dk_|and_ dv_ di|ensio|s, respe|tively. O|n each of thes|projec|ed versions of|
|queries, key|s|and val|<br>   ues w|<br>    e then perf|orm the|attention|functio|n in parallel, yi|elding_ d_|_v_-dimensional|
|output valu|es|. These|are c|oncatenat|ed and|once aga|in proje|cted, resulting|in the ﬁ|nal values, as|
|depicted in|Fi|gure 2.|||||||||
|<br>|<br>|<br>|||||||||
|Multi-head|at|tention|allow|s the mode|l to joi|ntly atten|d to infor|mation from d|ifferent|representation|
|subspaces a|t|differen|t posit|ions. With|a singl|e attentio|n head, a|veraging inhib|its this.||
|<br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>|<br>||
|4To illustr<br>|at<br>|e why th<br>|e dot p<br>|roducts get<br>|large, as<br>|sume that<br>|the comp<br>|onents of_ q_ and_ k_<br>|are inde|pendent random|
|variables wit|h|mean 0 a|nd var|iance 1. Th|en their|dot produc|t,_ q · k_ =|P_dk_<br>_i_=1 _qiki_, has|mean 0 a|nd variance_ dk_.|

