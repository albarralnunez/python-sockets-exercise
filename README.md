#Python concurrency#

##Statement##

* Develop a client which is able to send the information given at operations.

    * Dend the information using sockets to the service.
    * Receive information through the sockets and store the results in a file.

* Develop a service (python) which is build with the following features:

    * Receive information using sockets.
    * It is built by 2 different processes (at least). Consider having more processes to speed calculations.
    * Processes must be able to exchange information using PIPES. Please DO NOT use Threading or Pool.
    * Parent process must create and destroy child process for the arithmetic operations given at operations.
    * Once the arithmetic operation is finished on the second process, such process should be destroyed by the parent process.
    * Consider that operations should not be calculated using EVAL.
    * Consider using logging instead of console prints.

*The operations are in `mq/res/`*


##Solution##

*Below the approach of the proposed solution is explained.*

The system consist in a publisher(pub), a message broker(mq) and one consumer(con).
This architecture was chosen  to allow the consumer to solve the operations in a asynchronous way. We can send multiple files from the publisher, then the operations will be stored in the broker until the consumer is able to solved.
When the broker solve one of the operations, the solution are send to the broker. The broker is in charge of store the results in a file named results.txt (`mq/res/results.txt`)

