package com.github.code.admin.service.algorithm;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * @author CHENJIANHUA
 * @date 2019/7/10 11:07
 */
public class SelectionSort {
    public static List<Integer> sort(List<Integer> data) {
        if (null == data || data.size() <= 1) {
            return data;
        }
        for (int i = 0; i < data.size() - 1; i++) {
            int minIndex = i;
            for (int j = i + 1; j < data.size(); j++) {
                if (data.get(minIndex) > data.get(j)) {
                    minIndex = j;
                }
            }
            if(minIndex != i){
                Integer temp = data.get(i);
                data.set(i, data.get(minIndex));
                data.set(minIndex, temp);
            }
        }
        return data;
    }

    public static void main(String[] args) {
        List<Integer> testList = new ArrayList<>(Arrays.asList(13, 17, 11, 7, 19, 11, 5));
        List<Integer> sortedList = SelectionSort.sort(testList);
        for (Integer item : sortedList) {
            System.out.println("item: " + item);
        }
    }
}
