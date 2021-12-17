[![(inett GmbH)](https://www.inett.de/assets/images/icons/inett.x50.jpg)](https://www.inett.de/it-loesungen/checkmk)
# check_mk extension to check for log4j2 `CVE-2021-44228`

This Plugin wraps around
[logpresso/CVE-2021-44228-Scanner](https://github.com/logpresso/CVE-2021-44228-Scanner) 
([Apache License 2.0](https://github.com/logpresso/CVE-2021-44228-Scanner/blob/main/LICENSE))

### [How it works](https://github.com/logpresso/CVE-2021-44228-Scanner#how-it-works)
Run in 5 steps:
1. Find all .jar, .war, .ear, .aar files recursively.
2. Find `META-INF/maven/org.apache.logging.log4j/log4j-core/pom.properties` 
   entry from JAR file.
3. Read groupId, artifactId, and version.
4. Compare log4j2 version and print vulnerable version.
