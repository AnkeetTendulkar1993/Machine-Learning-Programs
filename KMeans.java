// Name: Ankeet Tendulkar
// KMeans Clustering Algorithm Implementation

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Random;

public class KMeans {

	/**
	 * @param args
	 */
	static File f;
	static FileReader fr;
	static FileWriter fw;
	static BufferedReader br;
	static ArrayList dataPointsOuter, dataPointsInner, clusterOuter1, clusterInner1, clusterOuter2, clusterInner2, clusterOuter3, clusterInner3;
	static double centroid[][], centroidOld[][];
	static double xMax,yMax,xMin,yMin,startX,startY;
	static Random randX,randY;
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			fr = new FileReader("src/km-data.txt");
			f = new File("src/Output_KMeans.txt");
			fw = new FileWriter(f,false);
			
			br  = new BufferedReader(fr);
			String s;
			xMax = Double.NEGATIVE_INFINITY;
			yMax = Double.NEGATIVE_INFINITY;
			xMin = Double.POSITIVE_INFINITY;
			yMin = Double.POSITIVE_INFINITY;
			dataPointsOuter = new ArrayList();
			while((s = br.readLine()) != null) {
				String temp[] = new String[2];
				temp = s.split(",");
				double xValue = Double.parseDouble(temp[0]);
				double yValue = Double.parseDouble(temp[1]);
				if(xValue > xMax) {
					xMax = xValue;
				}
				if(yValue > yMax) {
					yMax = yValue;
				}
				if(xValue < xMin) {
					xMin = xValue; 
				}
				if(yValue < yMin) {
					yMin = yValue; 
				}
				dataPointsInner = new ArrayList();
				dataPointsInner.add(new Double(xValue));
				dataPointsInner.add(new Double(yValue));
				dataPointsOuter.add(dataPointsInner);
			}
						
			String L1 = "L1";
			String L2 = "L2";
			
			// Euclidean Distance
			fw = new FileWriter(f,true);
			centroid = new double[3][2];
			centroidOld = new double[3][2];
			initializeCentroid();			
			System.out.println("----------------------- Euclidean Distance ------------------------");
			fw.append("----------------------- Euclidean Distance ------------------------\n");
			int iteration = 1;
			displayCentroids();
			while(!isEqual(centroid, centroidOld)) {
				System.out.println("Iteration " + iteration);
				fw.append("Iteration " + iteration + "\n");
				startProcess(L1);
				displayCentroids();
				iteration++;
			}
			displayFinalCentroid();
			System.out.println("==================================================================\n");
			fw.append("==================================================================\n");
			fw.close();
			
			// Manhattan Distance
			fw = new FileWriter(f,true);
			centroid = new double[3][2];
			centroidOld = new double[3][2];
			initializeCentroid();
			System.out.println("--------------------- Manhattan Distance -----------------------");
			fw.append("--------------------- Manhattan Distance -----------------------\n");
			iteration = 1;
			displayCentroids();
			while(!isEqual(centroid, centroidOld)) {
				System.out.println("Iteration " + iteration);
				fw.append("Iteration " + iteration + "\n");
				startProcess(L2);
				displayCentroids();
				iteration++;
			}	
			displayFinalCentroid();
			System.out.println("==================================================================\n");
			fw.append("==================================================================\n");
			fw.close();
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}		
	}
	
	public static void initializeCentroid() {
		
		// Use random class to make use of random variables
		randX = new Random();
		randY = new Random();
		startX = xMax - xMin;
		startY = yMax - yMin;
		//initialize centroids
		for(int i = 0; i < 3; i++) {
			centroid[i][0] = xMin + (randX.nextDouble() * startX) ;
			centroid[i][1] = yMin + (randX.nextDouble() * startY);
//			ArrayList t = (ArrayList)dataPointsOuter.get(i);
//			centroid[i][0] = Double.parseDouble(t.get(0) + "");
//			centroid[i][1] = Double.parseDouble(t.get(1) + "");
		}
	}
	
	public static void startProcess(String type) {
		storeOldCentroid();
		clusterOuter1 = new ArrayList();
		clusterOuter2 = new ArrayList();
		clusterOuter3 = new ArrayList();
		for(int i = 0; i < dataPointsOuter.size(); i++) {
			ArrayList t = (ArrayList)dataPointsOuter.get(i);
			String valX = (Double)t.get(0) + "";
			double x = Double.parseDouble(valX);
			String valY = (Double)t.get(1) + "";
			double y = Double.parseDouble(valY);
			int clusterIndex = 0;
			if(type.equals("L1"))
				clusterIndex = getEuclideanDistanceClosest(x,y);
			if(type.equals("L2"))
				clusterIndex = getManhattanDistanceClosest(x,y);
			insert(x,y,clusterIndex);
		}
		generateNewCentroids(clusterOuter1,0);
		generateNewCentroids(clusterOuter2,1);
		generateNewCentroids(clusterOuter3,2);
		//displayCluster1();
		//displayCluster2();
		//displayCluster3();
	}
	
	// Insert data points into specific clusters
	public static void insert(double x, double y, int index) {
		switch(index) {
			case 0: clusterInner1 = new ArrayList();
					clusterInner1.add(new Double(x));
					clusterInner1.add(new Double(y));
					clusterOuter1.add(clusterInner1);
					break;
				
			case 1: clusterInner2 = new ArrayList();
					clusterInner2.add(new Double(x));
					clusterInner2.add(new Double(y));
					clusterOuter2.add(clusterInner2);
					break;

			case 2: clusterInner3 = new ArrayList();
					clusterInner3.add(new Double(x));
					clusterInner3.add(new Double(y));
					clusterOuter3.add(clusterInner3);
					break;			
		}
	}
	
	public static void generateNewCentroids(ArrayList cluster, int clusterNumber) {
		double totalX = 0, totalY = 0;
		for(int i = 0; i < cluster.size(); i++) {
			ArrayList t = (ArrayList)cluster.get(i);
			String xVal = (Double)t.get(0)+"";
			double x = Double.parseDouble(xVal);
			String yVal = (Double)t.get(1)+"";
			double y = Double.parseDouble(yVal);
			totalX += x;
			totalY += y;
		}
		if(cluster.size() != 0) {
			centroid[clusterNumber][0] = totalX/cluster.size();
			centroid[clusterNumber][1] = totalY/cluster.size();		
		}
		else {
			centroid[clusterNumber][0] = 0.0;
			centroid[clusterNumber][1] = 0.0;
		}
		
	}
	
	public static int getEuclideanDistanceClosest(double x, double y) {
		double minDistance = Double.POSITIVE_INFINITY;
		int minClusterIndex = 0, i;
		for(i = 0; i < 3; i++) {			
			double distance = Math.sqrt(Math.pow(Math.abs(x - centroid[i][0]), 2) + Math.pow(Math.abs(y - centroid[i][1]), 2));
			if(distance < minDistance) {
				minDistance = distance;
				minClusterIndex = i;
			}
		}
		return minClusterIndex;
	}
	
	public static int getManhattanDistanceClosest(double x, double y) {
		double minDistance = Double.POSITIVE_INFINITY;
		int minClusterIndex = 0, i;
		for(i = 0; i < 3; i++) {			
			double distance = Math.abs(x - centroid[i][0]) + Math.abs(y - centroid[i][1]);
			if(distance < minDistance) {
				minDistance = distance;
				minClusterIndex = i;
			}
		}
		return minClusterIndex;
	}
	
	public static void storeOldCentroid() {
		for(int i = 0; i < 3; i++) {
			for(int j = 0; j < 2; j++) {
				centroidOld[i][j] = centroid[i][j];
			}
		}
	}
	
	public static boolean isEqual(double a[][], double b[][]) {
		for(int i = 0; i < 3; i++) {
			for(int j = 0; j < b[0].length; j++) {
				if(b[i][j] != a[i][j]) {
					return false;
				}
			}
		}
		return true;
	}
	
	public static void displayCluster1() {
		System.out.println("Cluster 1");
		for(int i = 0; i < clusterOuter1.size(); i++) {
			ArrayList t = (ArrayList)clusterOuter1.get(i);
			System.out.println(i + ": "+ (Double)t.get(0) + " " + (Double)t.get(1));
		}
	}
	
	public static void displayCluster2() {
		System.out.println("Cluster 2");
		for(int i = 0; i < clusterOuter2.size(); i++) {
			ArrayList t = (ArrayList)clusterOuter2.get(i);
			System.out.println(i + ": "+ (Double)t.get(0) + " " + (Double)t.get(1));
		}
	}
	
	public static void displayCluster3() {
		System.out.println("Cluster 3");
		for(int i = 0; i < clusterOuter3.size(); i++) {
			ArrayList t = (ArrayList)clusterOuter3.get(i);
			System.out.println(i + ": "+ (Double)t.get(0) + " " + (Double)t.get(1));
		}
	}
	
	public static void displayCentroids() {
		try {
			System.out.println("----- Old Centroid -----");
			fw.append("----- Old Centroid -----\n");
			for(int i = 0; i < 3; i++) {
				for(int j = 0; j < 2; j++) {
					System.out.print(centroidOld[i][j] + " ");
					fw.append(centroidOld[i][j] + " ");
				}
				System.out.println();
				fw.append("\n");
			}
			System.out.println("----- New Centroid -----");
			fw.append("----- New Centroid -----\n");
			for(int i = 0; i < 3; i++) {
				for(int j = 0; j < 2; j++) {
					System.out.print(centroid[i][j] + " ");
					fw.append(centroid[i][j] + " ");
				}
				System.out.println();
				fw.append("\n");
			}
			System.out.print("======================================\n");
			fw.append("======================================\n");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}		
	}
	
	public static void displayFinalCentroid() {		
		try {
			System.out.println("******** The Final Centroids Generated *********");
			fw.append("******** The Final Centroids Generated *********\n");
			for(int i = 0; i < 3; i++) {
				for(int j = 0; j < 2; j++) {
					System.out.print(centroid[i][j] + " ");
					fw.append(centroid[i][j] + " ");
				}
				System.out.println();
				fw.append("\n");
			}
			System.out.println("************************************************");
			fw.append("************************************************\n");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
}
