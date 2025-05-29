/**@file        modulo_reduction_traits.hpp
* @brief        编译期判断某整数能否被2整除
* @details      编译期判断某整数能否被2整除的类型结构体与编译期常量
* @author       neko
* @date         2025.5.29
* @version      V1.0
* @license      MIT
* @copyright    Copyright (c) 2025
*/


#include <type_traits>

namespace nekoc {
    /**@struct  modulo_reduction_traits
    * @brief    约束结构体
    * @details  定义约束实现与相关的便利类型，值
    */
    template<typename T,typename T t, typename std::enable_if_t<std::is_integral_v<T>,T> = 0>
    struct modulo_reduction_traits {
        using type = modulo_reduction_traits<T, t % 2>::type;
    };

    template<> 
    struct modulo_reduction_traits<int, 1> {
        using type = std::false_type;
    };

    template<>
    struct modulo_reduction_traits<int, 0> {
        using type = std::true_type;
    };

    template<typename T, T t> using modulo_reduction_traits_t = modulo_reduction_traits<T,t>::type;
    template<typename T, T t> constexpr bool modulo_reduction_traits_v = modulo_reduction_traits_t<T,t>::value;
}


