set nocompatible
set syntax=on
set autoindent
set tabstop=4
set softtabstop=4
set shiftwidth=4
set number
set nobackup
set noswapfile
set ruler
set langmenu=zh_CN.UTF-8
set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936
set termencoding=utf-8
set encoding=utf-8
source $VIMRUNTIME/delmenu.vim
source $VIMRUNTIME/menu.vim
language messages zh_CN.utf-8
set helplang=cn
filetype indent on
filetype plugin on
syntax enable
color slate
if has("gui_running")
  " Set a nicer font.
  set guifont=Consolas:h11:cDEFAULT
  " Hide the toolbar.
  set guioptions-=T
endif
map <F2> gg"+yG
map <F3> "+P
