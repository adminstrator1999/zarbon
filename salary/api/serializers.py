from rest_framework import serializers

from salary.models import Salary, FixedSalary


class SalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Salary
        fields = "__all__"


class SalaryGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Salary
        fields = "__all__"
        depth = 1


class FixedSalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = FixedSalary
        fields = "__all__"


class FlexibleSalarySerializer(serializers.Serializer):
    fixed_salary = serializers.DecimalField(max_digits=20, decimal_places=2)
    flexible_salary = serializers.DecimalField(max_digits=20, decimal_places=2)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

# for roles we have fixed salary
# for agents we have both fixed and flexible salary
# need to think about report


# we create profit according to the quantity we sell and we need filter date
