package com.github.code.admin.service.algorithm;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * @author CHENJIANHUA
 * @date 2019/7/10 11:07
 */
public class InsertionSort {
    public static List<Integer> sort(List<Integer> data) {
        if (null == data || data.size() <= 1) {
            return data;
        }
        for (int i = 1; i < data.size(); i++) {
            for (int j = 0; j < i; j++) {
                if (data.get(i) < data.get(j)) {
                    Integer temp = data.get(i);
                    data.set(i, data.get(j));
                    data.set(j, temp);
                }
            }
        }
        return data;
    }

    public static void main(String[] args) {
        List<Integer> testList = new ArrayList<>(Arrays.asList(13, 17, 11, 7, 19, 11, 5));
        List<Integer> sortedList = InsertionSort.sort(testList);
        for (Integer item : sortedList) {
            System.out.println("item: " + item);
        }
    }
}
