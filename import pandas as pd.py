import pandas as pd
import re
# initial_target_list = ['#AnnotateApplyAnnotationOption1',
# '#ai_WiresOutgoingRange_30',
# '#p_daa_k_WireOutCountries_20_157',
# '#BFI_DATA',
# '#AnnotateSaveOption1',
# '#MozgiApp-hypo-source-form-title',
# '#Hank_123-John_jones+-)(*&^%$#@!+=;:"?/|\\~`231',
# '27UDd(13mkKj']
fully_formatted_targets =[]
combined_new_clean_sanitized_targets  = []
sanitized_target_list = []
df = pd.read_csv(##dataset name here)
df = df.loc[df.INCLUDE_FOR_ANALYSIS, :]
#print(df.head(10))
for target in df['INPUT_TARGET']:
#for target in initial_target_list:
  # print("TARGET: ", target)
  ## Cleans targets, gets rid of all special characters +-)(*&^%$#@!+=;:"?/|\_~`
  if re.match(r'.*data.*\=', target):
    target = re.sub(r'.*data.*\=', '', target)
    #print("MATCHED DATA ATTRIBUTE PREFIX: ", target)
  target = re.findall(r'\d+|[A-Za-z]+', target)
  #print("TARGET: ", target)

  ## Removes empty items from the list as a result of the above regex findall
  item = list(filter(None, target))
  # print("ITEM: ", item)
  sanitized_target = []
  for component in item:
    # print("INDIVIDUAL ITEM: ", i)
    ## Finds 2 or more capital letters in item
    if(re.match('\w[A-Z][A-Z]\w*', component)):
      ## TODO: Handle when the two letters ID are placed together
      # print("IT MATCHES: ", i)
      ## Formats item to title case, 1st letter capital, all next letters lowercase
      component = component.title()
      # print("TITLED: ", i)
    # Splits the string on recognized capital letters
    broken_down_component = [a for a in re.split(r'([A-Z][a-z]*)', component) if a]
    # print("BROKEN DOWN COMPONENT: ", broken_down_component)
    sanitized_target.append(broken_down_component)
    # print("THE NEW TARGET: ", sanitized_target)
  sanitized_target_list.append(sanitized_target)
# print(sanitized_target_list)
for sanitized_item in sanitized_target_list:
  # print(item)
  new_clean_sanitized_target = []
  for sanitized_item_component in sanitized_item:
    # print(i)
    ## Checks if there is a sublist for the target
    if len(sanitized_item_component) > 1:
      # print("Inside sublist")
      ## Iterates on recognized sublist to create a flattened 1 dimensional list
      for borken_down_sanitized_item_component in sanitized_item_component:
        # print(sublist)
        new_clean_sanitized_target.append(borken_down_sanitized_item_component)
      # print(new_clean_target)
    else:
      new_clean_sanitized_target.append(sanitized_item_component[0])
  # print(new_clean_target)
  # print('**************************')
  combined_new_clean_sanitized_targets.append(new_clean_sanitized_target)
# print(combined_new_targets)
for new_clean_sanitized_target in combined_new_clean_sanitized_targets:
  fully_formatted_target = ''
  # print("LAST STRING: ", new_clean_sanitized_target)
  for new_clean_sanitized_target_component in new_clean_sanitized_target:
    # print("LAST STRING SINGLE: ", new_clean_sanitized_target_component)
    ## Forces all letters to lower case
    new_clean_sanitized_target_component = new_clean_sanitized_target_component.lower()
    # print("LOWERED ITEM: ", new_clean_sanitized_target_component)
    ## Adds underscore delimiters 
    fully_formatted_target = fully_formatted_target + '_' + new_clean_sanitized_target_component
  # print('**************************')
  ## Removes character from string, typically an _ because of how we concatenate the strings together
  fully_formatted_target = fully_formatted_target[1:]
  fully_formatted_targets.append(fully_formatted_target)
#print("THE NEW TARGETS: ", fully_formatted_targets)
df.insert(7,'CLEAN_INPUT_TARGETS',fully_formatted_targets)
print(df.head(10))
df.to_csv('cleaneduptargets.csv', index=False)