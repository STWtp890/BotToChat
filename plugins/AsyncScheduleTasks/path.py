import os

base_dir = os.path.abspath('.')
plugins_dir = os.path.join(base_dir, 'plugins')
AST_base_dir = os.path.join(plugins_dir, 'AsyncScheduleTasks')

if __name__ == '__main__':
	print(AST_base_dir)
