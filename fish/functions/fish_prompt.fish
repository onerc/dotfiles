function fish_prompt
    set_color yellow
    echo -n $USER
    set_color normal
    echo -n " at "
    set_color $fish_color_cwd
    echo -n (prompt_pwd)
    set_color normal
    echo -e \n'↪ '
end
# function fish_right_prompt
#     df -h | awk '$6 == "/" {print $3"/"$2}'
# end
