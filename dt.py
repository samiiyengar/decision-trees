#  _____    ______              _____      __  __   ______
# |  __ \  |  ____|     /\     |  __ \    |  \/  | |  ____|
# | |__) | | |__       /  \    | |  | |   | \  / | | |__
# |  _  /  |  __|     / /\ \   | |  | |   | |\/| | |  __|
# | | \ \  | |____   / ____ \  | |__| |   | |  | | | |____
# |_|  \_\ |______| /_/    \_\ |_____/    |_|  |_| |______|

'''
INSTRUCTIONS:
To run: $python dt.py [dataSetName]
Ex: $python dt.py set0.data
'''

import sys
import math


def read_input():
    '''
    We've done all of the file parsing here for you, since
    tedious file I/O is not the goal of this project.
    '''
    
    features = [] # all the attributes (as class objects)
    data = [] # all the data points
    dataSetName = "DATA SET NAME NOT INITIALIZED"
    with open(str(sys.argv[1]), 'r') as inFile:
        dataMode=False
        for line in inFile:
            if line[0] == "%":
                0  # do nothing
            elif line[:9] == "@relation":
                dataMode=False
                dataSetName = line[10:]
            elif line[:10] == "@attribute":
                dataMode=False
                newFeature = Feature()
                string = line[11:].split()
                newFeature.name = string[0]
                for val in string[1:]:
                    newFeature.vals.append(val.strip(','))
                newFeature.vals[-1] = newFeature.vals[-1][:-1]  # remove }
                newFeature.vals[0] = newFeature.vals[0][1:]  # remove {
                features.append(newFeature)
            elif line[:5] == "@data":
                dataMode = True
            elif dataMode == True:
                data.append([])
                for word in line.strip().split(','):
                    data[-1].append(word)
                data[-1][-1] = data[-1][-1].replace('\r\n', '')  # remove \r\n

    # print what was input to the program
    print("I found these attributes:")
    for feature in features:
        feature.debugInfo()
    print("\nI found these datapoints:")
    for datum in data:
        print ("  " + str(datum))

    return features, data, dataSetName



'''
class to pair attribute names with all allowed values
It's named "feature" to not be confused with "attribute" in the Node class
the attribute in Node class is of type string
'''
class Feature:
    def __init__(self):
        self.name = "  "
        self.vals = []

    def debugInfo(self):
        print("  "+self.name+str(self.vals))


class Node:
    def __init__(self,depth,attribute,attributeValue,dataPoints):

        # Values set on construction:
        self.depth=depth#depth of the node 0 is root (whole dataset)
        self.data=dataPoints#the list of data points belonging to this node
        self.children=[]#the list of Nodes that are children to this one

        # attribute is a string and not a Feature class because it has ONE value
        # the Feature class includes ALL possible values for input parsing.
        self.attribute = attribute#the attribute (e.g. color)
        self.attributeValue=attributeValue#the attribute VALUE (e.g. purple)


        # Value that must be set manually each time:
        self.category="NULL"#the category to assign at end (only for leaves)

        # the list of all attribute VALUES that were already selected before now
        # useful for knowing which can still be selected by
        self.ancestors=[]

    '''
    This will print the "pretty" version of the tree to file and terminal
    DO NOT CHANGE THIS!  This is 95% of the reason for the skeleton.
    This ensures that your program will output in the format we expect.
    '''
    def output_dt(self):
        string = ("|   " * (self.depth-1) + self.attribute + " = "
                + self.attributeValue + ": " + self.category + " ("
                + str(len(self.data)) + ")\n")
        if self.children==[]:
            return string
        for x in self.children:
            string = string + x.output_dt()
        return string

    '''
    This will print all the info of a Node and its children to terminal
    Use this only for debugging if necessary.
    '''
    def debugInfo(self):
        if self.children==[]: # leaf node
            print(self.attribute+":"+self.attributeValue
                  +"; depth="+str(self.depth)
                  +"; ancestors="+str(self.ancestors)
                  +"; cat="+str(self.category)+";\n"
                  +"data=" + str(self.data)+"\n")
        else:
            print(self.attribute+":"+self.attributeValue
                  +"; depth="+str(self.depth)
                  +"; ancestors=" + str(self.ancestors)+";\n"
                  +"data=" + str(self.data)+"\n")
        for c in self.children:
            c.debugInfo()

    '''
    This creates a child of the node it is called on.
    It requires the attribute, value, and data to populate itself.
    It sets the depth correctly to be one more than parent
    It places the child in the list of children of the parent.
    '''
    def createChild(self,attribute,attributeValue,dataPoints):
        self.children.append(Node(self.depth+1,attribute,
                                  attributeValue,dataPoints))
        self.children[-1].ancestors=self.ancestors+[self.attribute+":"+self.attributeValue]
        return self.children[-1]#returns child (by reference b/c Python)



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def total_entropy(data, output_categories):
    total_rows = len(data)
    dataset_entropy = 0
    for category in output_categories.vals:
        rows_with_category = [x for x in data if (x[-1] == category)]
        total_rows_with_category = len(rows_with_category)
        total_class_entropy = 0
        if total_rows_with_category > 0:
            total_class_entropy = -(float(total_rows_with_category)/total_rows) * math.log(float(total_rows_with_category)/total_rows)
        dataset_entropy = dataset_entropy + total_class_entropy
    return dataset_entropy

def feature_entropy(rows_with_feature, output_categories):
    total_rows = len(rows_with_feature)
    entropy = 0
    for category in output_categories.vals:
        rows_with_category = [x for x in rows_with_feature if (x[-1] == category)]
        total_rows_with_category = len(rows_with_category)
        category_entropy = 0
        if total_rows_with_category > 0:
            category_probability = float(total_rows_with_category) / total_rows
            category_entropy = - category_probability * math.log(category_probability)
        entropy = entropy + category_entropy
    return entropy

def feature_information_gain(feature, feature_index, data, output_categories):
    total_rows = len(data)
    information_gain = 0
    for feature_value in feature.vals:
        rows_with_feature = [x for x in data if (x[feature_index] == feature_value)]
        total_rows_with_feature = len(rows_with_feature)
        feature_value_entropy = feature_entropy(rows_with_feature, output_categories)
        feature_value_probability = float(total_rows_with_feature) / total_rows
        information_gain = information_gain + feature_value_probability * feature_value_entropy
    dataset_entropy = total_entropy(data, output_categories)
    return dataset_entropy - information_gain

def best_informative_feature(data, features, output_categories):
    features = features[:-1]
    max_gain = -1
    best_feature = None
    top_feature_index = -1
    feature_index = 0
    for feature in features:
        feature_gain = feature_information_gain(feature, feature_index, data, output_categories)
        if max_gain < feature_gain:
            max_gain = feature_gain
            best_feature = feature
            top_feature_index = feature_index
        feature_index = feature_index + 1
    return best_feature, top_feature_index

def build_subtree(root, feature, feature_index, output_categories):
    training_data = root.data
    for feature_value in feature.vals:
        rows_with_feature_value = [x for x in training_data if (x[feature_index] == feature_value)]
        pure_class = False
        for category in output_categories.vals:
            rows_with_category = [x for x in rows_with_feature_value if (x[-1] == category)]
            category_count = len(rows_with_category)
            if category_count == len(rows_with_feature_value):
                rows_without_category = [x for x in training_data if (x[feature_index] != feature_value)]
                training_data = rows_without_category
                subtree = root.createChild(feature.name, feature_value, rows_with_category)
                subtree.category = category
                pure_class = True
        if not pure_class and len(rows_with_feature_value) > 0 and len(rows_with_feature_value) != len(root.data):
            subtree = root.createChild(feature.name, feature_value, rows_with_feature_value)
    return training_data

def build_tree(root, data, features, output_categories):
    if len(data) == 0:
        return
    dataset_entropy = total_entropy(data, output_categories)
    # balanced dataset
    if dataset_entropy == 0:
        return
    top_feature, feature_index = best_informative_feature(data, features, output_categories)
    training_data = build_subtree(root, top_feature, feature_index, output_categories)
    for child in root.children:
        if child.category == "NULL":
            build_tree(child, child.data, features, output_categories)

# Fill in recursive algorithm here
def ID3(Node, features):
    for feature in features:
        print(feature.name)
        print(feature.vals)
    build_tree(Node, Node.data, features, features[-1])



def main():
    
    if len(sys.argv)!=2:
        print("ERROR: I need one argument, the input file.\n")

    ## read input file ##
    features, data, dataSetName = read_input()


    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # This is the main driver.  
    # You need to implement ID3 function

    rootNode=Node(0,"root","ROOT",data)
    ID3(rootNode, features)



    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    # This is needed to print your final tree.
    dt = rootNode.output_dt()
    print(dt)


if __name__ == "__main__":
    main()
