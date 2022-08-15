package org.example;

public class Main {
    public static void main(String[] args) {
        DeltaStandalone deltaStandalone = new DeltaStandalone();
        deltaStandalone.readDeltaTable(args[0], args[1]);
    }
}