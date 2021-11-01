
def boiler(csv_filename, output_path):
  
  from concepts import Context
  import pandas as pd
  import os
  
  print(os.getcwd())
  
  # create the context object from the csv file
  c = Context.fromfile(csv_filename, frmat='csv')
  
  # Define a function that returns the desired name for a concept. 
  # If the concept matches one vaccine extactly then use that. 
  # Otherwise use the concatenation of the attributes as the name.
  def get_concept_name(concept):
      if(len(concept.extent) == 1):
          # If there is only 1 vaccine captured by the concept
          # use that vaccine as the vaccine name
          nm = concept.extent[0]
      else:
          # otherwise use the attributes as a name
          nm = "; ".join(list(concept.intent))
      return nm
  
  concept_list = [a for a in c.lattice]
  concept_names = [get_concept_name(a) for a in concept_list]
  
  maps_to_list = []
  for idx, con in enumerate(concept_list):
      parent_concept_indexes = [concept_list.index(c) for c  in list(con.upper_neighbors)]
      for parent_idx in parent_concept_indexes:
          maps_to_list.append((idx, parent_idx))
          
  # create the concept table
  concept_df = pd.DataFrame({"id" : range(len(concept_names)), "concept_name" : concept_names})
  
  concept_relationship_df = pd.DataFrame({"id_1" : [x for x, _ in maps_to_list], 
                                          "relationship" : "Is a", 
                                          "id_2" : [x for _ , x in maps_to_list]})
                                          
  
  concept_df.to_csv(output_path + "concept.csv", index = False)
  concept_relationship_df.to_csv(output_path + "concept_relationship.csv", index = False)
