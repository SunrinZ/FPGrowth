#!/home/python/bin/python
#coding:utf8

def ShowFpnodeList(fpnode_list):	# Z 显示 FP 节点列表
	print '---------------------------'

	for fpnode in fpnode_list:
		print '(%s:%d)'%(fpnode.item, fpnode.f)

class FPNode:	# fp节点 属性
	def __init__(self):
		self.item = 'null'
		self.frequency = 0
		self.child_list = []
		self.next_pointer = None
		self.father= None

	def Print(self):
		print '(%s:%d)'%(self.item, self.frequency)
		for fpnode in self.child_list:
			fpnode.Print()

class Pointer:		# Point为空初始化
	def __init__(self):
		self.pointer_start = None
		self.pointer_end = None

class FPTree:
	def __init__(self):
		#头节点
		self.head = FPNode()	

	def Load(self, f_list, items_list, header_table):	# 加载数据信息
		for items in items_list:	# Z 熏黄数据行
			sorted_items  = []		# Z sort_items：项目排序
			for item in items:		# Z 循环每行中的数据项
				if len(sorted_items) == 0:	# 第一次添加
					sorted_items.append(item)
					continue
				idx = len(sorted_items) - 1 # Z index 坐标。
				while idx >= -1:
					if idx == -1:	# Z 第一次 append
						sorted_items.insert(idx+1, item)
						break;
					elif f_list[sorted_items[idx]] < f_list[item]:
						idx = idx - 1
					else:
						sorted_items.insert(idx+1, item)
						break;
			#items排序完毕。排序标准：
			#print sorted_items
			#构造
			now_level = 0
			now_head = self.head
			level = 0
			prefix_over = 0
			for item in sorted_items:
				level = level + 1
				fpnode_list = []
				self.GetLevelList(now_head, now_level, level, fpnode_list)
				#ShowFpnodeList(fpnode_list)

				fpnode = None
				if prefix_over == 0:
					fpnode = self.SearchInList(item, fpnode_list)

				#没有结点
				if fpnode == None:
					prefix_over = 1
					fpnode = FPNode()
					fpnode.item = item
					fpnode.frequency += 1
					fpnode.father = now_head
					now_head.child_list.append(fpnode)
					now_head = fpnode
					now_level = level

					#查找header
					header = None
					for i in range(0, len(header_table)):
						if header_table[i].item == item:
							header = header_table[i]
							break
					if header == None:
						print 'error!没找到header'
						exit
					if header.pointer.pointer_start == None:
						header.pointer.pointer_start = fpnode
						header.pointer.pointer_end = fpnode
					else:
						header.pointer.pointer_end.next_pointer = fpnode
						header.pointer.pointer_end = fpnode

				else:
					#找到节点继续搜索下一层
					now_head = fpnode
					now_level = level
					now_head.frequency += 1

	#搜索item的fpnode
	def SearchInList(self, item, fpnode_list):
		for fpnode in fpnode_list:
			if fpnode.item == item:
				return fpnode
		return None
		#raise
	#获取某一层节点列表
	def GetLevelList(self, this_fpnode,this_level, level, fpnode_list):
		if this_level == level:
			fpnode_list.append(this_fpnode)
			return

		for fpnode in this_fpnode.child_list:
			self.GetLevelList(fpnode, this_level + 1, level, fpnode_list)
			
	def Print(self):
		self.head.Print()
		

class Header:
	def __init__(self, item):
		self.item = item
		self.pointer = Pointer()
		self.frequency = 0

f_list = {'a':8, 'b':8, 'c':6, 'd':5, 'e':3}	# Z f_list表示 项目出现频次
print f_list

header_table = []
for item in f_list.keys():
	a_header = Header(item)
	header_table.append(a_header)



items_list = [['a','b'],['b', 'd', 'c'],['e','c','d','a'],['a', 'd', 'e'],
		['a', 'b', 'c'],['a','b','c','d'],['a'],['a','b','c'],['a','b','d'],['b','c','e']]
print items_list
#for item in items:
#	for item1 in item:
#		print item1
fp_tree = FPTree()	# Z 初始化FPTree-->初始化head
fp_tree.Load(f_list, items_list, header_table) #加载数据信息，生成FPTree
fp_tree.Print()

def ShowHeaderTable(header_table):
	for header in header_table:
		print header.item
		fpnode = header.pointer.pointer_start
		while fpnode != None:
			print '(%s:%d)'%(fpnode.item, fpnode.frequency)
			fpnode = fpnode.next_pointer

ShowHeaderTable(header_table)





