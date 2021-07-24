// $(document).ready(function () {
//   $.validator.addMethod("greaterThan",
//     function (value, element, params) {

//       if (!/Invalid|NaN/.test(new Date(value))) {
//         return new Date(value) > new Date($(params).val());
//       }

//       return isNaN(value) && isNaN($(params).val()) ||
//         (Number(value) > Number($(params).val()));
//     }, 'Must be greater than.');
//   // $("#addForm").validate({
//   //   rules: {
//   //     date_end: {
//   //       greaterThan: "#date_start"
//   //     }
//   //   }
//   // })
//   $("#date_end").rules('add', { greaterThan: "#date_start" });
// });