// Name: Ankeet Tendulkar
// Decision Tree Implementation

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;


public class DecisionTree {

	/**
	 * @param args
	 */
	static double attributeStatus[][];
	static String attributes[],decisionTreeData[][];
	static ArrayList inputData,Nodes,OriginalNodes,usedAttributes, inputDataOuter, inputDataInner, tempInputData;
	static File f;
	static FileReader fr;
	static FileWriter fw;
	static BufferedReader br;
	static ArrayList ifElseStatements;
	static LinkedHashMap statements, query;
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			fr = new FileReader("src/dt-data.txt");
			f = new File("src/Output_DecisionTree.txt");
			fw = new FileWriter(f,false);
			br = new BufferedReader(fr);
			
			//Processing the given input file
			String s = "";
			String firstLine = br.readLine().replaceAll("\\s","");
			attributes = (firstLine.substring(1, (firstLine.length()-1))).split(",");
			attributeStatus = new double[attributes.length][2];
			usedAttributes = new ArrayList();
	
			br.readLine();

			inputData = new ArrayList();
			while((s = br.readLine()) != null) {
				String line = s.replaceAll("\\s", "");
				String currentLine = line.substring(3, line.length() - 1);
				inputData.add(currentLine);
			}
			
			//Storing the given data in an ArrayList of ArrayLists
			decisionTreeData = new String[inputData.size()][];
			inputDataOuter = new ArrayList();
			for(int i = 0; i < inputData.size(); i++) {
				String currentRecord = (String)inputData.get(i);
				inputDataInner = new ArrayList();
				decisionTreeData[i] = currentRecord.split(",");
				for(int j = 0; j < decisionTreeData[i].length; j++) {
					inputDataInner.add(new String (decisionTreeData[i][j]));
				}
				inputDataOuter.add(inputDataInner);
			}
						
			String temp[] = new String[2];
			temp = labelDistribution().split(" ");
			double parentEntropy = calculateEntropy(temp);

			double max = Double.MIN_VALUE;
			String name = "";
			Nodes = new ArrayList();
			ifElseStatements = new ArrayList();
			
			//Creating nodes for each attribute and storing the distinct values they can take
			for(int i = 0; i < attributes.length - 1; i++) {
				Node n = new Node();
				ArrayList values = new ArrayList();
				ArrayList Inner = new ArrayList();
				
				n.attributeName = attributes[i];
				n.attributeIndex = i;
				for(int j = 0; j < inputData.size(); j++) {
					String attributeValue = new String(decisionTreeData[j][i]);
					if(!values.contains(attributeValue)) {
						values.add(attributeValue);
					}					
				}
				
				if(n.attributeStatus == 0) {					
					n.addPossibleValues(values);
					double b = calculateAttributeEntropy(n,n.values,i);
					n.InformationGain(parentEntropy - b);
					if(n.infoGain > max) {
						max = n.infoGain;
						name = n.attributeName;
					}
				}				
				Nodes.add(n);
			}
			
			// Keeping original copy of the Nodes
			OriginalNodes = new ArrayList();
			for(int i = 0; i < Nodes.size(); i++) {
				Node t = (Node)Nodes.get(i);
				Node o = new Node(t);
				OriginalNodes.add(o);
			}
			
			//Adding the root node to used attributes
			for(int k = 0; k < Nodes.size(); k++) {
				Node tem = (Node)Nodes.get(k);
				if(tem.attributeName.equals(name)) {
					usedAttributes.add(tem);
				}
			}
			
			// Generation of the tree from the root node
			Node u = (Node)usedAttributes.get(0);
			u.isRoot = true;
			statements = new LinkedHashMap();
			for(int i = 0; i < u.values.size(); i++) {
				reInitializeNodes();
				ArrayList tempInputData = new ArrayList();
				u.selectedAttributeValue = (String)u.values.get(i);
				statements.put(u.attributeName, u.selectedAttributeValue);
				String attribute = u.selectedAttributeValue;
				for(int j = 0; j < inputDataOuter.size(); j++) {
					ArrayList t = (ArrayList)inputDataOuter.get(j);
					if(attribute.equals(((String)t.get(u.attributeIndex)))) {
						tempInputData.add(t);
					}
				}							
				buildTree(u,i,tempInputData);
			}
						
			// Displaying compiled rules
			fw = new FileWriter(f,true);
			System.out.println("------------------------- Compiled Rules ------------------------------");
			fw.append("------------------------- Compiled Rules ------------------------------\n");
			Node start = u;
			ArrayList pathString = new ArrayList();
			dislayRulesUsingPointer(start, pathString);
			System.out.println("=======================================================================");
			fw.append("=======================================================================\n");
			fw.close();
			
			// display ifElseStatements
			fw = new FileWriter(f,true);
			System.out.println("------------- Stored If Else Rules in HashMap -------------------");
			fw.append("------------- Stored If Else Rules in HashMap -------------------\n");
			displayIfElseStatements();
			System.out.println("=================================================================");
			fw.append("=================================================================\n");
			fw.close();
			
			query = new LinkedHashMap();
			query.put("Size", "Large");
			query.put("Occupied", "Moderate");
			query.put("Price", "Cheap");
			query.put("Music", "Loud");
			query.put("Location", "City-Center");
			query.put("VIP", "No");
			query.put("Favourite Beer", "No");
			
			String key = u.attributeName;
			String val = (String)query.get(key);
			
			//Running Query
			fw = new FileWriter(f,true);
			System.out.println("--------- Result of query using the stored If Else Rules ---------");
			fw.append("--------- Result of query using the stored If Else Rules ---------\n");
			displayResultUsingCompiledRules(key,val);
			System.out.println("==================================================================");
			fw.append("==================================================================\n");
			fw.close();

			//Running Query
			fw = new FileWriter(f,true);
			System.out.println("---------- Result of query using Pointer on the tree ------------");
			fw.append("---------- Result of query using Pointer on the tree ------------\n");
			System.out.print("Path => ");
			fw.append("Path => ");
			displayResultUsingPointer(start);
			System.out.println("=================================================================");
			fw.append("=================================================================\n");
			fw.close();
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
		
	// Display the stored If Else rules
	public static void displayIfElseStatements() {
		try {	
			for(int i = 0; i < ifElseStatements.size(); i++) {
				LinkedHashMap t = (LinkedHashMap)ifElseStatements.get(i);
				System.out.println(t);
				fw.append(t + "\n");				
			}
		}
		catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
			
	}
	
	// Function to find the result of running the query using a pointer on the tree
	public static void displayResultUsingPointer(Node st) {
		try {	
			String value = (String)query.get(st.attributeName);
			System.out.print(st.attributeName + " = " + value + " ");
			fw.append(st.attributeName + " = " + value + " ");
			int index = st.values.indexOf(value);
			if(st.children.get(index).getClass().getCanonicalName().equals("Node")) {
				Node t = (Node)st.children.get(index);
				displayResultUsingPointer(t);
			}
			else {
				System.out.println();
				System.out.println("The result of the query = " + (String)st.children.get(index));
				fw.append("\nThe result of the query = " + (String)st.children.get(index) + "\n");				
				return;
			}	 
			return;
		}
		catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	// Function to calculate the result of the query using the stored rules
	public static void displayResultUsingCompiledRules(String key, String val) {
		try {
			for(int i = 0; i < ifElseStatements.size(); i++) {
				LinkedHashMap t = (LinkedHashMap)ifElseStatements.get(i);
		
				Object h[][] = new Object[2][];
				if(t.containsKey(key) && val.equals(t.get(key))) {
					h[0] = t.keySet().toArray();
					h[1] = t.values().toArray();
					int j;
					for(j = 0; j < h[0].length - 1; j++) {
						if(query.containsKey(h[0][j]) ) {
							if(!((String)query.get(h[0][j])).equals(h[1][j])) {
								break;
							}
						}
					}
					if(j == h[0].length - 1) {
						System.out.println("The result of the query = " + h[1][h[1].length - 1]);
						fw.append("The result of the query = " + h[1][h[1].length - 1] + "\n");
						break;
					}
				}
			}
		}
		catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}		
	}
	
	// Display rules by traversing 
	public static void dislayRulesUsingPointer(Node st, ArrayList path) {
		String currentNode = (String)st.attributeName;
		path.add(new String(currentNode));
		for(int i = 0; i < st.children.size(); i++) {
			if(st.children.get(i) != null) {
				String value = (String)st.values.get(i);
				path.add(new String(value));
				if(st.children.get(i).getClass().getCanonicalName().equals("Node")) {
					Node t = (Node)st.children.get(i);
					dislayRulesUsingPointer(t,path);
					path.remove(path.indexOf(value));
				}
				else {
					String result = (String)st.children.get(i);
					displayPath(path,result);
					path.remove(path.indexOf(value));
				}
			}
		}
		path.remove(path.indexOf(currentNode));
		return;
	}
	
	// Display the path to the result
	public static void displayPath(ArrayList path, String result) {		
		try {
			System.out.print("If ");
			fw.append("If ");
			for(int i = 0; i < path.size(); i++) {
				if(i%2 != 0) {
					System.out.print("= ");
					fw.append("= ");
				}
				System.out.print((String)path.get(i) + " ");
				fw.append((String)path.get(i) + " ");
			}
			System.out.print(" then Result = " + result);
			System.out.println();
			fw.append(" then Result = " + result + "\n");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}		
	}
	
	// Function used to construct the tree with recursive calls
	public static void buildTree(Node u, int attributeIndex, ArrayList tempInput) {
		ArrayList tempInputData = new ArrayList();	
		if(u.isRoot) {
			for(int i = 0; i < tempInput.size(); i++){
				ArrayList tempInputDataInner = new ArrayList();
				ArrayList tOuter = (ArrayList)tempInput.get(i);
				for(int j = 0; j < tOuter.size(); j++) {
					tempInputDataInner.add(new String((String)tOuter.get(j)));
				}
				tempInputData.add(tempInputDataInner);				
			}
		}
		if(!u.isRoot){			
			u.selectedAttributeValue = (String) u.values.get(attributeIndex);
			String attribute = u.selectedAttributeValue;
			for(int j = 0; j < tempInput.size(); j++) {
				ArrayList t = (ArrayList)tempInput.get(j);
				if(attribute.equals(((String)t.get(u.attributeIndex)))) {
					//System.out.println(t);
					tempInputData.add(t);
				}
			}
		}

		// Checking if the current set of records is Empty
		if(tempInputData.isEmpty()) {
			u.children.add(attributeIndex, null);
			return;
		}
		
		// Checking for terminal state
		String status[] = isTerminal(tempInputData).split(" ");
		if(!status[0].equals("notTerminal") && tempInputData.size() != 0) {
			u.children.add(attributeIndex, new String(status[0]));
			statements.put("Result", status[0]);
			ifElseStatements.add(statements.clone());			
			statements.remove("Result");
			return;			
		}
		String temporary[] = new String[2];
		temporary[0] = u.YesNo[attributeIndex][0] + "";
		temporary[1] = u.YesNo[attributeIndex][1] + "";
		u.valueSpecificEntropy[attributeIndex] = calculateEntropy(temporary);	
		
		for(int i = 0; i < Nodes.size(); i++) {
			Node n = (Node)Nodes.get(i);
			if(!usedAttributes.contains(n)) {				
				double e = calculateValueSpecificEntropy(n,tempInputData);	
				n.infoGain = u.valueSpecificEntropy[attributeIndex] - e;
			}
		}
		
		// Finding the node with maximum information gain
		Node tem = findMaximumInfoGain();
		usedAttributes.add(tem);
		tem.attributeStatus = 1;
		u.children.add(attributeIndex, tem);
		tem.parent = u;
		int i;
		for(i = 0; i < tem.values.size(); i++) {
			statements.put(tem.attributeName, (String)tem.values.get(i));
			buildTree(tem,i,tempInputData);
			reInitializeNodes();			
		}
		statements.remove(tem.attributeName);
		usedAttributes.remove(usedAttributes.indexOf(tem));
	}

	
	public static void displayHashMap(String status) {
		Iterator iterator = statements.keySet().iterator();
		System.out.print(" If ");  
		while (iterator.hasNext()) {
		   String key = iterator.next().toString();
		   String value = statements.get(key).toString();		  
		   System.out.print(key + " = " + value + " , ");
		}
		System.out.print(" => " + status);
		System.out.println();
	}
	
	// Checks if the set of records give a terminal state
	public static String isTerminal(ArrayList table) {
		int noOfYes = 0;
		int noOfNo = 0;
		
		for(int i = 0; i < table.size(); i++) {
			ArrayList row = (ArrayList)table.get(i);
			String result = (String)row.get(row.size() - 1);
			if(result.equals("No")) {
				noOfNo++;
			}
			if(result.equals("Yes")) {
				noOfYes++;
			}
		}
		if(table.size() == noOfNo) {
			return "No " + noOfYes + " " + noOfNo;
		}
		if(table.size() == noOfYes) {
			return "Yes " + noOfYes + " " + noOfNo;
		}
		return "notTerminal " + noOfYes + " " + noOfNo;
	}
	
	// Returns the node with Maximum information gain
	public static Node findMaximumInfoGain() {
		double max = Double.MIN_VALUE; 
		Node maxNode = new Node();
		for(int i = 0; i < Nodes.size(); i++) {
			Node t = (Node)Nodes.get(i);
			if(!usedAttributes.contains(t)) {
				if(t.infoGain > max) {
					max = t.infoGain;
					maxNode = t;
				}
			}
		}
		if(!maxNode.attributeName.equals(""))
			return maxNode;
		else 
			return null;
	}
	
	// Gives number of Yes or No in the original table
	public static String labelDistribution() {
		int numOfNo = 0;
		int numOfYes = 0;

		int indexEnjoy = decisionTreeData[0].length - 1;
		for(int i = 0; i < decisionTreeData.length; i++) {
			if((decisionTreeData[i][indexEnjoy]).equals("Yes")) {
				numOfYes++;
			}
			else {
				numOfNo++;
			}
		}
		return (numOfYes + " " + numOfNo);
	}
	
	// Calculates the entropy
	public static double calculateEntropy(String[] t) {
		double numOfYesNo[] = new double[2];
		numOfYesNo[0] = Double.parseDouble(t[0]);
		numOfYesNo[1] = Double.parseDouble(t[1]);
		if((numOfYesNo[0] == 0) || (numOfYesNo[1] == 0)) {
			return 0.0;
		}
		double probability1 = numOfYesNo[0]/ (numOfYesNo[0] + numOfYesNo[1]);
		double probability2 = numOfYesNo[1]/(numOfYesNo[0]+numOfYesNo[1]);
		double p1,p2;
		if(probability1 != 0)
			p1 = probability1 * (Math.log10(1/probability1) / Math.log10(2));
		else p1 = 0;
		if(probability2 != 0)
			p2 = probability2 * (Math.log10(1/probability2) / Math.log10(2));
		else p2 = 0;
		return (p1 + p2);		
	}
	
	// Calculates the entropy for selecting the root attribute
	public static double calculateAttributeEntropy(Node n, ArrayList t, int attributeIndex) {
		int YesNo[][] = new int[t.size()][3];
		int total = 0;
		double localEntropy[] = new double[t.size()];
		for(int j = 0; j < t.size(); j++) {
			String currVal = (String)t.get(j);
			for(int i = 0; i < inputData.size(); i++) {				
				if(decisionTreeData[i][attributeIndex].equals(currVal)) {
					if((decisionTreeData[i][attributes.length - 1].equals("Yes")))
						YesNo[j][0]++;
					else YesNo[j][1]++;
				}
			}
			YesNo[j][2] = YesNo[j][0] + YesNo[j][1];
			total += YesNo[j][2];
			String temp[] = new String[2];
			temp[0] = YesNo[j][0] + "";
			temp[1] = YesNo[j][1] + "";
			localEntropy[j] = calculateEntropy(temp);
		}
		n.storeYesNo(YesNo);
		double entropy = 0.0;
		for(int j = 0; j < t.size(); j++) {
			entropy = entropy + (((double)YesNo[j][2] / total) * localEntropy[j]);
		}
		
		return entropy;
	}
	
	public static double calculateValueSpecificEntropy(Node n, ArrayList tempInputData) {
		double localEntropy[] = new double[n.values.size()];
		n.YesNo = new int[n.values.size()][3];
		for(int i = 0; i < tempInputData.size(); i++) {
			ArrayList t = (ArrayList)tempInputData.get(i);
			String val = (String)t.get(n.attributeIndex);
			// Index of a particular value of attribute
			int indexOfValue = n.values.indexOf(val);
			String result = (String)t.get(((ArrayList)tempInputData.get(0)).size() - 1);
			if(result.equals("Yes")) {
				n.YesNo[indexOfValue][0]++;
			}
			else {
				n.YesNo[indexOfValue][1]++;
			}
		}
			
		double total = 0.0;
		for(int i = 0; i < n.values.size(); i++) {
			n.YesNo[i][2] = n.YesNo[i][0] + n.YesNo[i][1];
			total += n.YesNo[i][2];
			String temp[] = new String[2];
			temp[0] = n.YesNo[i][0] + "";
			temp[1] = n.YesNo[i][1] + "";
			localEntropy[i] = calculateEntropy(temp);			
		}
		double entropy = 0.0;
		for(int i = 0; i < n.values.size(); i++) {
			if(localEntropy[i] != 0)
				entropy = entropy + (((double)n.YesNo[i][2] / total) * localEntropy[i]);
		}
		return entropy;
	}
	
	// Used to reinitialize the set of Nodes
	public static void reInitializeNodes() {
		Nodes = new ArrayList();
		for(int j = 0; j < OriginalNodes.size(); j++) {
			Node r = (Node)OriginalNodes.get(j);
			Node n = new Node(r);
			Nodes.add(n);
		}
	}	
}

// Class used for representing each attribute as a node
class Node {
	ArrayList values = new ArrayList();
	double valueSpecificEntropy[];
	int YesNo[][];
	Node child[], parent = null;
	ArrayList children;
	boolean isRoot = false;
	
	int attributeStatus, attributeIndex, valSize;
	String attributeName ,selectedAttributeValue;
	double infoGain = 0.0;
	
	public Node() {
		this.attributeName = "";
	}
	
	public Node(Node a) {
		this.values = (ArrayList)a.values.clone();
		this.selectedAttributeValue = a.selectedAttributeValue;
		this.attributeName = a.attributeName;
		this.children = (ArrayList)a.children.clone();
		this.isRoot = a.isRoot;
		this.parent = a.parent;
		this.attributeIndex = a.attributeIndex;
		this.attributeStatus = a.attributeStatus;
		this.infoGain = a.infoGain;
		this.YesNo = (int[][])a.YesNo.clone();
		this.valueSpecificEntropy = (double[])a.valueSpecificEntropy.clone();
	}
	
	public void addPossibleValues(ArrayList temp) {
		values = (ArrayList)temp.clone();
		valueSpecificEntropy = new double[values.size()];
		valSize = values.size();
		children = new ArrayList();
	}
	
	public void calculateEntropy() {
		for(int i = 0; i < values.size(); i++) {
			String a = (String)values.get(i);
		}
	}	
	
	public void InformationGain(double t) {
		this.infoGain = t;
	}
	
	public void storeYesNo(int t[][]) {
		this.YesNo = (int[][]) t.clone();
	}
}
