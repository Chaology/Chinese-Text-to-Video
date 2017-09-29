def format_text(string):
    words=string.split()
    output=''
    buffer_string=''
    for w in words:
        if(len(buffer_string)<50):
            buffer_string+=w+' '
        else:
            output+=buffer_string+'\n'
            buffer_string=w+' '
    output+=buffer_string   
    return output
