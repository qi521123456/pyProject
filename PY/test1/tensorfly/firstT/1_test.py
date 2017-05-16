import tensorflow as tf

def test1():
    matrix1 = tf.constant([[3.,3.]])
    matrix2 = tf.constant([[2.],[2.]])
    product = tf.matmul(matrix1,matrix2)
    sess = tf.Session()
    result = sess.run(product)
    print([result])
    sess.close()
def test2():
    sess = tf.InteractiveSession()
    x = tf.Variable([1.0,2.0])
    a = tf.constant([3.0,3.0])
    x.initializer.run()
    sub = tf.sub(x,a)
    print(sub.eval())
def test3():
    state = tf.Variable(0, name="counter")
    one = tf.constant(1)
    new_value = tf.add(state, one)
    update = tf.assign(state, new_value)
    init_op = tf.initialize_all_variables()
    # 启动图, 运行 op
    with tf.Session() as sess:
        # 运行 'init' op
        sess.run(init_op)
        # 打印 'state' 的初始值
        print(sess.run(state))
        # 运行 op, 更新 'state', 并打印 'state'
        for _ in range(4):
            sess.run(update)
            print(sess.run(state))
def test4():
    input1 = tf.constant(3.0)
    input2 = tf.constant(2.0)
    input3 = tf.constant(5.0)
    intermed = tf.add(input2, input3)
    mul = tf.mul(input1, intermed)
    with tf.Session() as sess:
        result = sess.run([mul, intermed])
        print(result)
def test5():
    input1 = tf.placeholder(tf.float32)
    input2 = tf.placeholder(tf.float32)
    output = tf.mul(input1, input2)
    with tf.Session() as sess:
        print(sess.run([output], feed_dict={input1: [7.], input2: [2.]}))


test5()