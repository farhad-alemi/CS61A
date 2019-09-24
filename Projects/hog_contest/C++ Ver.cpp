#include <iostream>
#include <iomanip>
using namespace std;
double six_sided(double outcome)
{
    if (1 <= outcome <= 6)
        return 1.0 / 6.0;
    else
        return 0.0;
}

double roll_a_one(double n)
{
    /*"""The probability of rolling a 1 from N dice.

    >> > [round(roll_a_one(n), 3) for n in range(1, 10)]
    [0.167, 0.306, 0.421, 0.518, 0.598, 0.665, 0.721, 0.767, 0.806]
"""*/
    if (n == 0)
        return 0;
    return six_sided(1) + (1 - six_sided(1)) * roll_a_one(n - 1);
}

double roll_no_ones(double total, double n)
{
    /*"""The probability of scoring total from N dice, assuming no ones.

    >> > [round(roll_no_ones(t, 2), 3) for t in range(1, 13)]
    [0.0, 0.0, 0.0, 0.028, 0.056, 0.083, 0.111, 0.139, 0.111, 0.083, 0.056, 0.028]
"""*/
    double outcome;
    double chance;
    if (total == 0 and n == 0)
        return 1;
    else if (n == 0)
        return 0;
    else
    {
        chance = 0;
        outcome = 2;
    }
    while (outcome <= 6)
    {
        chance += six_sided(outcome) * roll_no_ones(total - outcome, n - 1);
        outcome += 1;
    }
    return chance;
}

double roll_dice(double total, double n)
/*"""The probability of scoring total from N dice, observing pig out.

    >> > [round(roll_dice(t, 2), 3) for t in range(1, 13)]
    [0.306, 0.0, 0.0, 0.028, 0.056, 0.083, 0.111, 0.139, 0.111, 0.083, 0.056, 0.028]
"""*/
{
    if (total == 1)
        return roll_a_one(n);
    else
        return roll_no_ones(total, n);
}
double roll_at_least(double k, double n)
{
        /*"""Return the chance of scoring at least K points by rolling N dice
        without rolling a 1.

        >> > round((5 / 6) * *4, 10)
        0.4822530864
        >> > round(roll_at_least(8, 4), 10)
        0.4822530864
        >> > round(roll_at_least(4, 4), 10)
        0.4822530864
        >> > round(roll_at_least(20, 4), 10)
        0.0540123457
        >> > round(roll_at_least(20, 6), 10)
        0.3017189643
        >> > round(roll_at_least(8, 2), 10)
        0.4166666667
        """*/
    double total = k;
    double chance = 0;
    while (total <= 6.0 * n)
    {
        chance += roll_dice(total, n);
        total += 1;
    }
    return chance;
}

int main()
{
    cout << std::setprecision(10);
    

    for (int n = 1; n < 11; ++n)
    {
        for (int k = 1; k < 61; ++k)
        {
            cout << roll_at_least(k, n) << ", ";
        }
        cout << endl;
    }
}