# No need to process files and manipulate strings - we will
# pass in lists (of equal length) that correspond to 
# sites views. The first list is the site visited, the second is
# the user who visited the site.

# See the test cases for more details.

def highest_affinity(site_list, user_list, time_list):
   # Returned string pair should be ordered by dictionary order
   # I.e., if the highest affinity pair is "foo" and "bar"
   # return ("bar", "foo"). 
   result = []  
   site_dict = {}
   site_order = []
   site_counter = 0
   # set ID for each site
   for a in site_list:
      if a not in site_dict:
         site_dict[a] = site_counter
         site_order.append(a)
         site_counter += 1
   user_dict = dict()
   user_counter = 0
   for a in user_list:
      if a not in user_dict.keys():
         user_dict[a] = [site_dict[site_list[user_counter]]]
      else: 
         temp_user_list = user_dict.get(a)
         if temp_user_list.count(site_dict[site_list[user_counter]]) == 0:
            temp_user_list.append(site_dict[site_list[user_counter]])
         user_dict[a] = temp_user_list
      user_counter += 1
   # site-site mapping
   site_map = [[0 for i in range(site_counter)] for j in range(site_counter)]

   max_value = 0
   max_index = [0,0]
   for a in user_dict.keys():
      temp_user_list = user_dict.get(a)
      temp_user_list.sort()
      for m in range(len(temp_user_list)):
         for n in range (m+1,len(temp_user_list)):
            if temp_user_list[m] < temp_user_list[n]:
               site_map[temp_user_list[m]][temp_user_list[n]] += 1
               if site_map[temp_user_list[m]][temp_user_list[n]] >= max_value:
                  max_value = site_map[temp_user_list[m]][temp_user_list[n]]
                  max_index[0] = temp_user_list[m]
                  max_index[1] = temp_user_list[n]

   result.append(site_order[max_index[0]])
   result.append(site_order[max_index[1]])
   if site_order[max_index[0]] > site_order[max_index[1]]:
      result[0] = site_order[max_index[1]]
      result[1] = site_order[max_index[0]]  
   return (result[0], result[1])
        
