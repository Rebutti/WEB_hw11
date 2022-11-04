# first_name = request.form.get('first_name')
# last_name = request.form.get('last_name')
# birthday = request.form.get('birthday')
# email = request.form.get('email')
# address = request.form.get('address')
# cell_phone = request.form.get('cell_phone')

# print(first_name, last_name,birthday,email,address,cell_phone)
# if first_name == '':
#     flash('You should write your first name')
#     return redirect(request.url)

def contact_validation(first_name, last_name, birthday, email, address, cell_phone):
    result = 'You should write\n'
    flag = False
    if first_name == '':
        flag = True
        result +='first name\n'
    if last_name == '':
        flag = True
        result +='last name\n'
    if flag == True:
        return result[:-1]