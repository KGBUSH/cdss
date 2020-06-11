# 字典问题
阵发性##ext_freq 室上速##Disease 心动过速##Symptom 





# 现有问题

持续性##ext_freq 闷##x 胀痛##ext_texture

疼痛持续不缓解
 疼痛##Symptom 持续##vd 不##v 缓解##ext_intensity 
  第2:0个逗号句子
	 {'symptom': '疼痛', 'target': '自身', 'duration': None, 'intensity': '缓解', 'exist': '有'}



患者##n 病来##v 无##v 胸##ng 背部##Bodypart 撕裂样##ext_texture 疼痛##Symptom
建议胸背部，每次都合并到一起（高优先级）


近2年体重下降30kg
 近##t 2##m 年##m 体重##BasicInfo 体重下降##Symptom 30##m kg##eng 
  第6:0个逗号句子
	 {'symptom': '体重下降', 'target': '自身', 'duration': '近2年', 'exist': '有'}



不##d 伴##v 肢体##Bodypart 体乏##Symptom 乏力##Symptom
建议处理：应该一起合并目前是'体乏力'


2##m 周前##t 患者##n 因##c 劳累##Symptom 后##x 再次##ext_freq 发作##ext_freq 胸痛##Symptom 不适##Symptom ，
劳累应该作为一个条件，导致某种symptom


近半年体重增加约5kg
5KG没有识别到：	 {'symptom': '体重增加', 'target': '自身', 'duration': '近半年', 'exist': '有'}


持续##vd 约##d 1##m 小##a 时##ng 后##f 自行##v 缓解##ext_intensity
，无心悸、气促，持续约1小时后自行缓解，来我科就诊  
没有识别出来


胸骨##Bodypart 下段##Bodypart 以及##c 剑突##Bodypart 部位##n 觉##v 闷痛##ext_texture 痛感##Symptom 
建议合并



后脑##n 勺##q 不适##Symptom
{'symptom': '不适', 'target': '自身', 'duration': None, 'exist': '有', 'accompany': '有'} 后脑勺没识别出来










