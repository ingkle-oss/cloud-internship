package org.example;

import io.delta.standalone.DeltaLog;
import io.delta.standalone.data.CloseableIterator;
import io.delta.standalone.data.RowRecord;
import java.time.Duration;
import java.time.Instant;
import org.apache.hadoop.conf.Configuration;

public class DeltaStandalone {
    public DeltaStandalone() {}

    public void readDeltaTable(String accessKey, String secretKey) {
        String endPoint = "minio.minio.svc.cluster.local";
        Configuration conf = new Configuration();
        conf.set("fs.s3a.access.key", accessKey);
        conf.set("fs.s3a.secret.key", secretKey);
        conf.set("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider");
        conf.set("fs.s3a.path.style.access", "true");
        conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem");
        conf.set("fs.s3a.endpoint", endPoint);
        conf.set("fs.s3a.connection.ssl.enabled", "false");
        DeltaLog log = DeltaLog.forTable(conf, "s3a://delta/test");
        CloseableIterator<RowRecord> dataIter = log.update().open();
        System.out.println("start...");
        Instant start = Instant.now();

        try {
            while(dataIter.hasNext()) {
                RowRecord var8 = (RowRecord)dataIter.next();
            }

            dataIter.close();
        } catch (Exception var11) {
            System.out.println("Error");
            System.exit(1);
        }

        Instant end = Instant.now();
        long elapsedTime = Duration.between(start, end).toMillis();
        System.out.println("Complete, Time elapsed(ms): " + elapsedTime);
    }
}
